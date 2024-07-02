# encoding: utf-8

import pymssql
import config as cfg
import time

def connect():
    print '> [db] Connecting...'
    conn = pymssql.connect(cfg.SERVER, cfg.USER, cfg.PASSWORD, cfg.DATABASE)
    cursor = conn.cursor()
    print '> [db] Connect ok'
    return cursor


def getDeviceTimeSeries(cursor, device, start, end, filter=True):
    #print '> [db.getDeviceTimeSeries] Fetching device %012x data, (%d, %d)...'% (device, start, end)
    date = time.localtime(start)
    date_end = time.localtime(end)
    if date.tm_mday != date_end.tm_mday:
        print '> [db.getDeviceTimeSeries] Start and end timestamps are not on the same day'
    day = '%04d%02d%02d' % (date.tm_year, date.tm_mon, date.tm_mday)
    table = 'tb_node_report_%s' % day
    _filter = ''
    if filter:
        _filter = '_filter'
    query = ''' SELECT dt_localtime, id_node, vl_rss%s
                FROM %s WITH(NOLOCK)
                WHERE dt_localtime >= %d and dt_localtime <= %d
                        and id_node >= %d and id_node <= %d
                        and id_device = %d
                ORDER BY dt_localtime''' \
            % (_filter, table, start, end, 
                    0xac8674000000, 0xac8674ffffff,
                    device)
    _t_start = time.time()
    cursor.execute(query)
    data = cursor.fetchall()
    #print '> [db.getDeviceTimeSeries] Done. Got %d rows in %fs' % (len(data), time.time()-_t_start)
    return data


def runQuery(cursor, query):
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def getDeviceTimeSeries1(cursor, device, start, end, meraki=False, filter=False):
    #print '> [db.getDeviceTimeSeries] Fetching device %012x data, (%d, %d)...'% (device, start, end)

    date = time.localtime(start)
    date_end = time.localtime(end)
    if date.tm_mday != date_end.tm_mday:
        print '> [db.getDeviceTimeSeries] Start and end timestamps are not on the same day'
    _filter = ''
    if filter:
        _filter = '_filter'
    day = '%04d%02d%02d' % (date.tm_year, date.tm_mon, date.tm_mday)
    table = 'tb_node_report_%s' % day

    interval = 'dt_localtime >= %d and dt_localtime <= %d' \
            % (start, end)

    nodes = '(id_node >= %d and id_node <= %d)' \
            % (0xac8674000000, 0xac8674ffffff)
    if meraki == True:
        nodes += ' or (id_node = %d) or (id_node = %d)' \
                % (0x180A81479E, 0x180A8147F4)

    query = ''' SELECT dt_localtime, id_node, vl_rss%s
                FROM %s WITH(NOLOCK)
                WHERE (%s) and (%s) and id_device = %d
                ORDER BY dt_localtime''' \
            % (_filter, table, interval, nodes, device)

    _t_start = time.time()
    data = runQuery(cursor, query)

    #print '> [db.getDeviceTimeSeries] Done. Got %d rows in %fs' % (len(data), time.time()-_t_start)
    return data


def setDeviceLocation(cursor, data, start, end):
    date = time.localtime(start)
    date_end = time.localtime(end)
    if date.tm_mday != date_end.tm_mday:
        print '> [db.setDeviceLocation] Start and end timestamps are not on the same day'
    day = '%04d%02d%02d' % (date.tm_year, date.tm_mon, date.tm_mday)
    table = 'tb_SECTOR_NEAR_%s' % day
    query_header = ''' INSERT INTO %s
                       (id_sector, id_device, dt_localtime, vl_x, vl_y, vl_node_count)
                       VALUES 
                   ''' % (table)
    #print '> [db.setDeviceLocation] Inserting %d rows into %s, (%d, %d)...' \
    #        % (len(data), table, start, end)
    _t_start = time.time()
    step = 1000
    fmt = '(%d, %d, %d, %f, %f, %d)'
    for n in range(len(data)/step):
        entries = [fmt % x for x in data[n*step:(n+1)*step]]
        query_body = ','.join(entries)
        cursor.execute(query_header + query_body)
    if len(data) % step:
        entries = [fmt % x for x in data[-(len(data)%step):]]
        query_body = ','.join(entries)
        cursor.execute(query_header + query_body)
    cursor.connection.commit()
    #print '> [db.setDeviceLocation] Done in %fs' % (time.time()-_t_start)
