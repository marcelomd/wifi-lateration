#!/usr/bin/env python
# encoding: utf-8


from collections import OrderedDict
from eq import doCalibration, doLateration, dbm2m
from itertools import combinations
from numpy.linalg import norm
from random import randrange
from requests import post   
import datetime as dt
import db
import numpy as np
import time
import json


nodes = {
        0xac86741082d8: {'index': 0, 'x': (00.00, 00.00)},
        0xac867410be10: {'index': 1, 'x': (12.42, 00.00)},
        0xac867410be28: {'index': 2, 'x': (24.77, 00.00)},
        0xac867410ea10: {'index': 3, 'x': (38.79, 00.00)},
        0xac86741ca318: {'index': 4, 'x': (00.00, 11.12)},
        0xac867410be08: {'index': 5, 'x': (12.42, 11.12)},
        0xac86741ca350: {'index': 6, 'x': (24.77, 11.12)},
        0xac86741082b0: {'index': 7, 'x': (38.79, 11.12)},
        0xac86741ca330: {'index': 8, 'x': (28.59, 22.42)},
}

headers = {'Content-Type': 'application/json'}

date = dt.date(2014, 07, 3)
db.connect()


while True:
    time.sleep(2)
    time_series = OrderedDict()
    raw_data = db.getDeviceNow(date, 0xAC86741CA357)
    if not raw_data:
        print 'No data'
        continue

    ts = (raw_data[-1][0] / 10) * 10
    for row in raw_data:
        timestamp = 0
        node = row[1]
        rssi = row[2]
        time_series.setdefault(timestamp, {})
        time_series[timestamp].setdefault(node, []).append(rssi)

    _t_start = time.time()

    for timestamp, data in time_series.iteritems():
        if len(data) < 2:
            continue

        #timespan = (timestamp - start) / 600 # 10 in 10 minutes
        #k, n = calibration_table[timespan]
        k = -8
        n = 3.
        r = [ts, # timestamp
                0., 0., # x y
                k, n,   # k, n
                0., 0., 0., 0.,  0., 0., 0., 0.,  0.] # nodes start at 5
        _pos = []
        _rssi = []

        for node, rssi in data.iteritems():
            avg = (float(sum(rssi)) / float(len(rssi)))
            r[nodes[node]['index']+5] = dbm2m(avg, k, n)
            _pos.append(nodes[node]['x'])
            _rssi.append(avg)
        pos = np.array(_pos)
        rssi = np.array(_rssi)

        x, y = doLateration(pos, rssi, k, n)
        r[1] = x
        r[2] = y

    print '> Run time:', time.time() - _t_start
    print r
    data = json.dumps(r)
    response = post(
            url='http://127.0.0.1:5000/put',
            data=str(data), headers=headers,
            timeout=10
    )