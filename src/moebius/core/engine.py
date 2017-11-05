# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:23:34 2017
@author: Jérémie Fache
"""
import numpy as np
import rx
from rx import Observable
from moebius.bus.messages import (BM, READY, ready, oftype)
from . import api


class Engine():
    def __init__(self, busMessage8):
        main_scheduler = rx.concurrency.EventLoopScheduler()
        input_R8 = (busMessage8
                    .observe_on(main_scheduler)
                    .filter(oftype(status=READY))
                    )


        ascan8 = (input_R8
                  .filter(oftype('engine/ASCAN_CHANGE'))
                  .map(ASCAN_node))

        energy8 = (ascan8
                   .filter(oftype('engine/ASCAN', status=READY))
                   .map(lambda bm: ENERGY_node(bm))
                   )

        discrete_streams = [input_R8.filter(oftype('engine/STEP'))]
        discrete8 = rx.Observable.combine_latest()


        output8s = [ascan8, energy8]

        self._output8 = Observable.merge(output8s)

    @property
    def output8(self):
        return self._output8






def ENERGY_node(bm):
    signals_array = bm.payload.data
    energy_array = compute_energy(signals_array)
    rbm = bm._replace(tag='engine/ENERGY', payload=energy_array)
    return rbm


def ASCAN_node(bm):
#    if bm.tag == 'engine/ASCAN_CHANGE':
    # TODO: test for shape for sources if any

    rbm = bm._replace(tag='engine/ASCAN')

    return rbm


def compute_energy(signals_array):
    return np.sum(signals_array **2, axis=0)

