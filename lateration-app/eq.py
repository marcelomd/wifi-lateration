#!/usr/bin/env python
# encoding: utf-8

import numpy as np
from numpy.linalg import norm
from lmfit import Parameter, Parameters, minimize


def dbm2m(rssi, k, n):
    return 10. ** ((k - rssi) / (10. * n))

def m2dbm(m, k, n):
    return k -10. * n * np.log10(m)


def distanceResidual(params, dist, rssi):
    k = params['k'].value
    n = params['n'].value
    #model = m2dbm(dist, k, n)
    #return (model - rssi) / dist**2
    model = dbm2m(rssi, k, n)
    return (model - dist) / dist**2


def doCalibration(dist, rssi, method='leastsq'):
    params = Parameters()
    params.add('k', value=-30., max=0.)
    params.add('n', value=2.5, min=2., max=6.)
    result = minimize(distanceResidual,
            params, args=(dist, rssi),
            method=method)
    return (params['k'].value, params['n'].value)


def laterationResidual(params, pos, rssi, k, n):
    x = params['x'].value
    y = params['y'].value
    dist = dbm2m(rssi, k, n)
    model = norm(pos-(x,y), axis=1)
    return (model - dist) / dist


def doLateration(pos, rssi, k, n, method='leastsq'):
    if len(pos) < 2:
        return None
    params = Parameters()
    params.add('x', value=0.)
    params.add('y', value=0.)
    result = minimize(laterationResidual,
            params, args=(pos, rssi, k, n),
            method=method)
    return (params['x'].value, params['y'].value)

