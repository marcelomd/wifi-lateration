#!/bin/bash
# encoding: utf-8

import numpy as np
from do import doCalibration, doLateration
import pymssql
from time import time


device = 158434847220163
nodes = {
        189693472849408: 0, # AC867410BE00
        189693472834216: 1, # AC86741082A8
        189693472849440: 2, # AC867410BE20
        189693472860712: 3, # AC867410EA28
        189693472860704: 4, # AC867410EA20
        189693473629040: 5, # AC86741CA370
}

table = "tb_node_report_tmp_20140610"
database = "dbLocalTrackingLab"
server = "177.71.248.102"
user = "localtrackinglabservico"
password = "@ocivresbalgnikcartlacol!"


conn = pymssql.connect(server, user, password, database)
cursor = conn.cursor()


def getDevices(cursor, date):
    day = '20140629'
    start = 12345678
    end = 12345679
    query = ''' SELECT id_device
                FROM tb_node_report_%s
                WHERE dt_localtime >= %d and dt_localtime <= %d'''
            % (day, start, end)
    print '> Fetching devices for %s, (%d, %d)...'% (day, start, end)
    cursor.execute(query)
    _t_start = time()
    devices = cursor.fetchAll()
    print '> Done. Got %d devices in %d' % (len(devices), time()-_t_start)








