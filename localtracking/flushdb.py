#! /usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from time import sleep
from config import db_flush_interval, db_flush_limit


def flush(limit):
    r = urlopen('http://listenerservice.elasticbeanstalk.com/flushdb?limit=%d' % limit)
    r.close()


if __name__ == '__main__':
    while(True):
        sleep(db_flush_interval)
        flush(db_flush_limit)
