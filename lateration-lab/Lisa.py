#!/usr/bin/env python
# encoding: utf-8
import os
import config as cfg
import db
import cPickle as pickle
from collections import OrderedDict
import numpy as np
import time
from scipy.spatial.distance import canberra


def buildMap():
    print '> Building fingerprint...'
    device = cfg.REFERENCE_DEVICE
    cursor = db.connect()
    fingerPrint = {}

    for point in cfg.FINGERPRINT:
        start, end = cfg.FINGERPRINT[point]['time']
        raw_data = db.getDeviceTimeSeries(cursor, device, start, end)
        time_series = OrderedDict()
        for row in raw_data:
            timestamp = row[0]
            node = row[1]
            rssi = float(row[2])
            time_series.setdefault(node, [])
            time_series[node].append(rssi)

        mean = [1000] * len(cfg.NODES)
        median = [1000] * len(cfg.NODES)
        std = [1000] * len(cfg.NODES)
        count = [1000] * len(cfg.NODES)

        for node, rssi in time_series.iteritems():
            index = cfg.NODES[node]['index']
            mean[index] = np.mean(rssi)
            median[index] = np.median(rssi)
            std[index] = np.std(rssi)
            count[index] = len(rssi)

        fingerPrint[point] = {
                'mean': mean,
                'median': median,
                'std': std,
                'count': count
        }

    cursor.connection.close()

    fdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), cfg.SITE_NAME+'.pickle')
    f = open(fdir, 'wb')
    pickle.dump(fingerPrint, f)
    f.close()

    print '> Done. Saved in', cfg.SITE_NAME+'.pickle'


def main(device, start, end):
    print 'Running location for device %012x...'% device

    fdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), cfg.SITE_NAME+'.pickle')
    f = open(fdir, 'rb')
    fingerPrint = pickle.load(f)
    f.close()
    for point in cfg.FINGERPRINT:
        fingerPrint[point]['mean'] = np.array(fingerPrint[point]['mean'])
        fingerPrint[point]['median'] = np.array(fingerPrint[point]['median'])
        fingerPrint[point]['std'] = np.array(fingerPrint[point]['std'])
        fingerPrint[point]['count'] = np.array(fingerPrint[point]['count'])
    
    cursor = db.connect()
    raw_data = db.getDeviceTimeSeries(cursor, device, start, end)
    if not raw_data:
        print '> No data'
        return

    t_start = time.time()
    time_series = OrderedDict()
    for row in raw_data:
        #timestamp = row[0]
        timestamp = (row[0] / 10) * 10
        node = row[1]
        rssi = row[2]
        time_series.setdefault(timestamp, {})
        time_series[timestamp].setdefault(node, []).append(rssi)

    results = []
    for timestamp, data in time_series.iteritems():
        if len(data) < 2:
            continue

        _sig = [0.] * len(cfg.NODES)
        for node, rssi in data.iteritems():
            _sig[cfg.NODES[node]['index']] = (float(sum(rssi)) / float(len(rssi)))
        sig = np.array(_sig)

        r = []
        for i in fingerPrint:
            r.append((canberra(sig, fingerPrint[i]['mean']), i))
        r.sort()
        sector = cfg.FINGERPRINT[r[0][1]]['sector']
        x = 0
        y = 0
        count = 0
        results.append((sector, device, timestamp, x, y, count))

    db.setDeviceLocation(cursor, results, start, end)
    cursor.connection.close()

    print '> Location for %012x complete in %fs' % (device, time.time()-t_start)
    print '> Done'
    return results


if __name__ == '__main__':
    import sys

    if sys.argv[1] == 'buildmap':
        exit(buildMap())

    device = int(sys.argv[1], 16)
    start = int(sys.argv[2])
    end = int(sys.argv[3])
    main(device, start, end)

