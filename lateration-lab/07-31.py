#!/usr/bin/env python
# encoding: utf-8

import os
import config as cfg
import db
import cPickle as pickle
from collections import OrderedDict
import numpy as np
import pandas as pd
import time
from scipy.spatial.distance import canberra, cityblock, euclidean, mahalanobis
from pandas.core.nanops import nanmean, nanmedian
from scipy.spatial.distance import canberra
from collections import Counter
import Lisa

cursor = db.connect()

def setTarget(data):
    if not isinstance(data, pd.Timestamp):
        return np.nan
    for point in cfg.FINGERPRINT:
        start = pd.to_datetime(cfg.FINGERPRINT[point]['time'][0], unit='s')
        end = pd.to_datetime(cfg.FINGERPRINT[point]['time'][1], unit='s')
        if start <= data <= end:
            return cfg.FINGERPRINT[point]['sector']
    return np.nan


def hit(data, col):
    if np.isnan(data['target']):
        return np.nan
    if np.isnan(data[col]):
        return np.nan
    if data[col] == data['target']:
        return 1
    return 0


def locate(data, period='10s', metric='mean', knn=1, fps=None):
    fp = period+'_'+metric
    r = None
    r = [(canberra(data, sample), sector) for sample, sector in fps[fp]]
    r.sort()
    count = Counter(x[1] for x in r[:knn])
    return count.most_common()[0][0]


def getPoint(cursor, device,
        start, end,
        period='10s', how=nanmean,
        meraki=False, filter=False):
    columns = None
    if meraki:
        columns = range(11)
    else:
        columns = range(9)
    index = pd.to_datetime(range(start, end+1), unit='s')
    df = pd.DataFrame(index=index, columns=columns, dtype=float)
    raw_data = db.getDeviceTimeSeries1(cursor, device,
            start, end,
            meraki=meraki, filter=filter)
    for row in raw_data:
        rssi = row[2]
        if rssi < -127 or rssi >= 0:
            continue
        node = row[1]
        t = pd.to_datetime(row[0], unit='s')
        df.loc[t][cfg.NODES[node]['index']] = rssi
    return df.resample(period, how=how)


def do(meraki, filter, period, sample_period, knn):
    fps = None
    fps_path = 'ref_'
    columns = range(9)
    if meraki:
        fps_path += 'meraki_'
        columns = range(11)
    if filter:
        fps_path += 'filter_'
    else:
        fps_path += 'raw_'
    fps_path += 'data'

    print fps_path.replace('ref', 'htc')
    with open(fps_path.replace('ref', 'htc')+'.pickle', 'rb') as f:
        points = pickle.load(f)

    fps_path += '_fps.pickle'
    print fps_path
    with open(fps_path, 'rb') as f:
        fps = pickle.load(f)
    
    device = 0xd8b377d2c8e5
    result = []

    for point in points:
        start = point[0]
        end = point[1]
        sector = point[2]
        raw_data = point[3]

        index = pd.to_datetime(range(start, end+1), unit='s')
        df = pd.DataFrame(index=index, columns=columns, dtype=float)

        for row in raw_data:
            rssi = row[2]
            if rssi < -127 or rssi >= 0:
                continue
            node = row[1]
            t = pd.to_datetime(row[0], unit='s')
            df.loc[t][cfg.NODES[node]['index']] = rssi

        df_mean = df.resample(sample_period, how=nanmean)
        df_median = df.resample(sample_period, how=nanmedian)
        df = df.resample(sample_period, how=nanmean)

        r_mean_mean     = df_mean.apply(locate, axis=1, metric='mean', period=period, knn=knn, fps=fps)
        r_mean_median   = df_mean.apply(locate, axis=1, metric='median', period=period, knn=knn, fps=fps)
        r_median_mean   = df_median.apply(locate, axis=1, metric='mean', period=period, knn=knn, fps=fps)
        r_median_median = df_median.apply(locate, axis=1, metric='median', period=period, knn=knn, fps=fps)

        df['target'] = pd.Series(df.index, index=df.index).apply(setTarget)

        df['r_mean_mean']       = r_mean_mean
        df['r_mean_median']     = r_mean_median
        df['hit_mean_mean']     = df.apply(hit, axis=1, col='r_mean_mean')
        df['hit_mean_median']   = df.apply(hit, axis=1, col='r_mean_median')

        df['r_median_mean']     = r_median_mean
        df['r_median_median']   = r_median_median
        df['hit_median_mean']   = df.apply(hit, axis=1, col='r_median_mean')
        df['hit_median_median'] = df.apply(hit, axis=1, col='r_median_median')
        result.append(df)

    df = pd.concat(result, axis=0)
    name = 'ref_'
    if meraki:
        name += 'meraki_'
    if filter:
        name += 'filter_'
    name += period + sample_period + str(knn) + '.xlsx'
    print name
    writer = pd.ExcelWriter(name)
    df.to_excel(writer,'result')
    writer.save()

    print '>', period, sample_period, knn, meraki, filter, ':'
    print df['hit_mean_mean'].value_counts(normalize=True)
    print df['hit_mean_median'].value_counts(normalize=True)
    print df['hit_median_mean'].value_counts(normalize=True)
    print df['hit_median_median'].value_counts(normalize=True)



#for meraki in [True, False]:
for meraki in [False, True]:
    for filter in [False, True]:
        for period in ['10s', '20s', '30s', '60s']:
            for sample_period in ['10s', '20s', '30s', '60s']:
                for knn in [1, 3, 5, 7, 9]:
                    do(meraki, filter, period, sample_period, knn)

"""
#device = 0x90187cc9e1c3
device = 0xd8b377d2c8e5
columns = range(len(cfg.NODES)-2)
cursor = db.connect()
for knn in [1, 3, 5, 7, 9]:
    for sample_period in ['10s', '20s', '30s', '60s']:
        for period in ['10s', '20s', '30s', '60s']:
            result = []
            for point in cfg.FINGERPRINT:
                start, end = cfg.FINGERPRINT[point]['time']
                sector = cfg.FINGERPRINT[point]['sector']
                df = getPoint(cursor, device, start, end, sample_period, nanmean)

                df_mean = getPoint(cursor, device, start, end, sample_period, nanmean)
                df_median = getPoint(cursor, device, start, end, sample_period, nanmedian)

                r_mean_mean     = df_mean.apply(locate, axis=1, metric='mean', period=period, knn=knn)
                r_mean_median   = df_mean.apply(locate, axis=1, metric='median', period=period, knn=knn)
                r_median_mean   = df_median.apply(locate, axis=1, metric='mean', period=period, knn=knn)
                r_median_median = df_median.apply(locate, axis=1, metric='median', period=period, knn=knn)

                df['target'] = pd.Series(df.index, index=df.index).apply(setTarget)

                df['r_mean_mean']       = r_mean_mean
                df['r_mean_median']     = r_mean_median
                df['hit_mean_mean']     = df.apply(hit, axis=1, col='r_mean_mean')
                df['hit_mean_median']   = df.apply(hit, axis=1, col='r_mean_median')

                df['r_median_mean']     = r_median_mean
                df['r_median_median']   = r_median_median
                df['hit_median_mean']   = df.apply(hit, axis=1, col='r_median_mean')
                df['hit_median_median'] = df.apply(hit, axis=1, col='r_median_median')
                result.append(df)

            df = pd.concat(result, axis=0)
            writer = pd.ExcelWriter(str(device)+period+sample_period+str(knn)+'.xlsx')
            df.to_excel(writer,'result')
            writer.save()

            print '>', period, sample_period, knn
            print df['hit_mean_mean'].value_counts(normalize=True)
            print df['hit_mean_median'].value_counts(normalize=True)
            print df['hit_median_mean'].value_counts(normalize=True)
            print df['hit_median_median'].value_counts(normalize=True)

"""
