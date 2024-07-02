#!/bin/bash
# encoding: utf-8

import numpy as np
from numpy.linalg import norm
from itertools import combinations
from collections import OrderedDict
import time
import datetime as dt
from eq import doCalibration, doLateration
import db

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

# Distances between nodes
nodeXnode = {}
n = combinations(sorted(nodes.keys()), 2)
for pair in n:
    nodeXnode[pair] = norm(np.array(nodes[pair[0]]['x']) - np.array(nodes[pair[1]]['x']))


##### MAIN

date = dt.date(2014, 06, 29)
db.connect()

##### Calibrate environment
calibration_data = OrderedDict() # calibrations data = {timespan: {pair: [rssi]}}
node_data = db.getNodeData(date)
start, _ = db.get_times(date)
for row in node_data:
    t = (row[0] - start) / 600 # 10 in 10 minutes
    node0 = row[1] & 0xfffffffffff8 # clear last 3 bits
    node1 = row[2] & 0xfffffffffff8 # clear last 3 bits
    if node0 < node1:
        pair = (node0, node1)
    else:
        pair = (node1, node0)
    rssi = row[3]
    calibration_data.setdefault(t, {})
    calibration_data[t].setdefault(pair, []).append(rssi)

calibration_table = {}
for timespan, data in calibration_data.iteritems():
    _dist = []
    _rssi = []
    for pair, values in data.iteritems():
        avg = float(sum(values)) / float(len(values)) # Simple average
        _dist.append(nodeXnode[pair])
        _rssi.append(avg)
    dist = np.array(_dist)
    rssi = np.array(_rssi)
    calibration_table[timespan] = doCalibration(dist, rssi, method='cobyla')


del node_data
del calibration_data

##### Get master device list
devices = db.getDevices(date)


##### Purge device list



##### Filter



##### Trilaterate
for device in devices:
    raw_data = db.getDeviceTimeSeries(date, device)
    time_series = OrderedDict()
    
    for row in raw_data:
        timestamp = (row[0] / 10) * 10
        node = row[1]
        rssi = row[2]
        time_series.setdefault(timestamp, {})
        time_series[timestamp].setdefault(node, []).append(rssi)
    
    for timestamp, data in time_series.iteritems():
        for node, rssi in data.iteritems():
            avg = (float(sum(rssi)) / float(len(rssi)))
            time_series[timestamp][node] = avg

    _t_start = time.time()
    results = []
    for timestamp, data in time_series.iteritems():
        if len(data) < 2:
            continue

        timespan = (row[0] - start) / 600 # 10 in 10 minutes
        k, n = calibration_table[timespan]
        _pos = []
        _rssi = []

        for node, rssi in data.iteritems():
            _pos.append(nodes[node]['x'])
            _rssi.append(rssi)
        pos = np.array(_pos)
        rssi = np.array(_rssi)

        x, y = doLateration(pos, rssi, k, n)

    run_time = time.time() - _t_start
    del raw_data
    del time_series
    print '> Lateration %012x: %d' % (device, run_time)


