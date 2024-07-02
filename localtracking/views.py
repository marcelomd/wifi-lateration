# -*- coding: utf-8 -*-

from flask import Blueprint, make_response, redirect, request, Response

import config
from report_pb2 import Report, Station
from database import db
from sqlalchemy import and_
from models import AP, Device, NodeReport
from config import db_flush_limit

import os, sys
from time import time, ctime, asctime
from json import loads, dumps
from binascii import hexlify

api = Blueprint('api', __name__)


##### Errors
@api.errorhandler(404)
def not_found(error):
    """Simple 404 error response."""
    return make_response('ERROR', 404)


##### Stats
aps = set()     # List of seen APs
apstats = {}    # AP stats. Tuples (last report, last timestamp)
filestats = {}  # Number of downloads per requested file

@api.route('/summary')
def summary():
    """Simple summary of application statistics.
    Used mostly for development.
    """
    ap_count = AP.query.count()
    dev_count = Device.query.count()
    report_count = NodeReport.query.count()

    s = 'Summary:\n'
    s += '  Time: %s (%d)\n' % (asctime(), time())
    s += '  Database row count:\n'
    s += '    APs: %d, Devices: %d, Reports: %d\n' % (ap_count, dev_count, report_count)
    s += '  Download:\n'
    s += '    %s\n' % filestats
    s += '  Access Points:\n'
    s += '    Seen: %d\n' % len(aps)
    s += '    [    MAC     ] Last report              - Last timestamp     \n'
    for ap, stats in apstats.iteritems():
        if stats[0] == 0:
            lr = '                        '
            lt = '                        '
            delta = 0;
        else:
            lr = ctime(stats[0])
            lt = ctime(stats[1])
            delta = int(time() - stats[0])
        s += '    [%s] %s - %s - %d\n' % (ap.upper(), lr, lt, delta)
    return Response(s, mimetype='text/plain')


##### Static files
bucket = 'http://s3-sa-east-1.amazonaws.com/' + os.environ.get('AWS_BUCKET_NAME') + '/public/'

@api.route('/public/<f>')
def public(f):
    """Simply redirect public file requests to S3.
    I'm sure there's a better way to do it.
    """

    s = filestats.setdefault(f, 0)  # Increment download counter
    filestats[f] = s + 1
    return redirect(bucket + f)     # Redirect to S3. Ideally the HTTP server should do it


##### reset
@api.route('/reset')
def db_reset():
    """Resets database and application statistics."""

    # Reset globals
    global aps
    global apstats
    global filestats
    aps = set()
    apstats = {}
    filestats = {}

    # Reset DB
    db.drop_all()
    db.create_all()

    # Register APs
    for a in config.aps:
        mac = a['mac']
        name = a['name']
        lat = a['lat']
        lng = a['lng']
        ap = AP(mac, name, lat, lng)
        db.session.add(ap)
        mac = "%012x" % mac
        apstats[mac.upper()] = (0, 0)   # Add AP to stats
    db.session.commit()
    print 'App reset requested!'
    return 'Ok'


##### Flush DB
@api.route('/flushdb')
def flushdb():
    """Flush older entries to keep query times short."""

    limit = request.args.get('limit', db_flush_limit, type=int)
    now = int(time())
    NodeReport.query.filter(NodeReport.t < now - limit).delete()
    db.session.commit()
    print "flush requested %d" % limit
    return 'Ok'


##### Receive reports from nodes
def bytes2int(mac):
    """Converts byte array to integer."""

    return int(mac.encode('hex'), 16)


@api.route('/reports', methods=['POST'])
def reports():
    """Receives report from AccessPoints.
    Format is defined in report.proto.
    """

    report = Report()
    report.ParseFromString(request.data)

    mac = bytes2int(report.mac)
    ap = AP.query.filter_by(mac=mac).first() # Ignore unregistered APs
    if not ap:
        print "strange mac reporting: %012x" % mac
        return 'OK', 201

    now = int(time())

    # Stats
    report_timestamp = report.timestamp
    report_mac = hexlify(report.mac).upper()
    apstats[report_mac] = (now, report_timestamp) # Received time, reported time
    aps.add(report.mac)

    # Process stations
    for sta in report.stations:
        # This is probably a performance bottleneck.
        # Trying to add an unique entry in a multithreaded world is hard.
        # We commit at each step, as there are, potentially, a hundred rows
        # to add at every call and we don't want to rollback and redo everything.
        # TODO: Look into savepoints.
        mac = bytes2int(sta.mac)

        # Add device to DB. Watch out for race conditions
        dev = Device.query.filter_by(mac=mac).first()
        if not dev:
            try:
                dev = Device(mac=mac)
                db.session.add(dev)
                db.session.commit()
            except:
                db.session.rollback()
                dev = Device.query.filter_by(mac=mac).first()
                print 'Error adding device: %012x' % mac

        t = sta.timestamp
        if t < 86400:
            # Sometimes a node sends reports before synchronizing its clock.
            t = now
        rss = 0 - (sta.rssi/sta.count)
        count = sta.count
        r = NodeReport(t=t, rss=rss, count=count, ap=ap, dev=dev,)
        db.session.add(r)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        print 'Error adding reports'

    return 'OK', 201


##### Dump reports table
@api.route('/dump')
def dump():
    """Snapshot of 'reports' table.
    Useful for debug.
    """

    s = ''
    for report in NodeReport.query.\
            options(db.joinedload(NodeReport.dev), db.joinedload(NodeReport.ap)).\
            all():
        s += str(report) + '</br>'
    return s


##### Access point/RSSI by device in a given timeframe.
@api.route('/devreports')
def devreports():
    """Returns a list of device sightings, with every Access Point that saw
    the device (and its RSSI value) in a given timeframe.

    The format of the returned JSON is as follows:

    [{"mac": "AC867410EA1F",        # Device's MAC address
      "loc": {"lat": -30.086121,    # Device's latitude
              "lng": -51.245982,    # Device's longitude
              "levelId": 2,         # Device's floor
              "prec": 2},           # ?
      "lrrt": 2,                    # Seconds before current time
      "rss": {"AC867410EA20": -42,  # Access Point's MAC Addres / RSSI
              "AC867410EA10": -34,
              "AC867410EA30": -51,
              "AC867410BE10": -78,
              "AC867410BE00": -58}
     },
     ...
    ]
    """
    average = request.args.get('mean', 'yes', type=str)
    max_lrrt = request.args.get('lrrt', 8, type=int) # 8s is the de facto default.
    now = int(time())
    limit = now - max_lrrt

    tmp = {}
    # Pull all sightings from last lrrt. Group reports by device MAC, AP MAC, like this:
    # {
    #   device.mac:
    #   {
    #       'rss':
    #       {
    #           ap.mac: [report.rss, report.rss, report.rss, ...],
    #           ...
    #       }
    #   },
    #   ...
    # }
    for report in NodeReport.query.\
            options(db.joinedload(NodeReport.dev), db.joinedload(NodeReport.ap)).\
            filter(and_(NodeReport.t >= limit, NodeReport.t <= now)).\
            order_by(NodeReport.t.desc()):

        ap = '%012x' % report.ap.mac
        dev = '%012x' % report.dev.mac
        tmp.setdefault(dev, {'rss': {}, 't': report.t})
        tmp[dev]['rss'].setdefault(ap, []).append(report.rss)

    response = []
    loc = {'lat': 1.0, 'lng': 1.0, 'levelId': 2, 'prec': 2}
    for device_mac, entry in tmp.iteritems():
        point = {}
        point['loc'] = loc
        point['mac'] = device_mac
        point['lrrt'] = now - entry['t']
        if average == 'yes': # Do average
            entry['rss'].update((ap_mac, sum(rss_list)/len(rss_list)) for ap_mac, rss_list in entry['rss'].iteritems())
        else: # Get last RSS
            entry['rss'].update((ap_mac, rss_list[0]) for ap_mac, rss_list in entry['rss'].iteritems())
        point['rss'] = entry['rss']
        response.append(point)
    return dumps(response)


##### Add APs
@api.route('/ap', methods=['POST'])
def ap_add():
    """Insert Access Point into database.
    Other Access Points reporting will be ignored.

    Input format:
    {"mac": "00:11:22:33:44:55",    # MAC address
     "name": "abc",                 # Display name
     "lat": "0.123",                # Latitude
     "lng": "4.567"}                # Longitude
    """

    a = loads(request.data)
    mac = int(a['mac'].translate({ord(u':'):None}), 16)
    lat = float(a['lat'])
    lng = float(a['lng'])

    ap = AP.query.filter_by(mac=mac).first()
    if not ap:
        try:
            ap = AP(mac=mac, name=a['name'], lat=lat, lng=lng)
            db.session.add(ap)
            db.session.commit()
            return 'Ok'
        except:
            db.rollback()
            print traceback.format_exc()
            print 'error adding %012x' % mac
            return 'Error'

