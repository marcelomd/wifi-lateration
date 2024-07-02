#!/usr/bin/env python
# encoding: utf-8


import numpy as np
from numpy.linalg import norm
from lmfit import Parameter, Parameters, minimize

from collections import OrderedDict
from copy import deepcopy
from time import time

import pymssql


def dbm2m(rssi, k, n):
    return 10. ** -((rssi + k) / (10. * n))

def m2dbm(m, k, n):
    return k + 10. * n * np.log10(m)



def distanceResidual(params, dist, rssi):
    k = param['k'].value
    n = param['n'].value

    model = m2dbm(dist, k, n)

    return (model - rssi) / dist


def laterationResidual(params, pos, rssi, k, n):
    x = params['x'].value
    y = params['y'].value

    dist = dbm2m(rssi, k, n)
    model = norm(pos-(x,y), axis=1)

    return (model - dist) / dist


def doCalibration(dist, rssi, method='leastsq'):
    params = Parameters()
    params.add('k', value=20., min=20., max=50.)
    params.add('n', value=2., min=2., max=6.)
    result = minimize(distanceResidual,
            params, args=(dist, rssi),
            method=method)
    return (result['k'], result['n'])


def doLateration(pos, rssi, k, n):
    if len(pos) < 2:
        return None
    params = Parameters()
    params.add('x', value=0.)
    params.add('y', value=0.)
    result = minimize(laterationResidual,
            params, args=(pos, rssi, k, n),
            method=method)
    return (result['x'].value, result['y'].value)

