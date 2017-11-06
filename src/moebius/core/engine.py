# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:23:34 2017
@author: Jérémie Fache
"""
import numpy as np
import rx
from rx import Observable
from moebius.bus.messages import (BM, READY, ready, error, oftype, combine_seeds)
from . import api


class Engine():
    def __init__(self, busMessage8):
        main_scheduler = rx.concurrency.EventLoopScheduler()
        input_R8 = (busMessage8
                    .observe_on(main_scheduler)
                    .filter(oftype(status=READY))
                    )

        ascanR8 = input_R8.filter(oftype('ASCAN', READY))

#        ascan8 = (input_R8
#                  .filter(oftype('engine/ASCAN_CHANGE'))
#                  .map(ASCAN_node))

#        energy8 = (ascan8
#                   .filter(oftype('engine/ASCAN', status=READY))
#                   .map(lambda bm: ENERGY_node(bm))
#                   )
        energy_node = node(function=compute_energy,
                           tag='ENERGY',
                           scheduler=rx.concurrency.thread_pool_scheduler)

        energy8 = (ascanR8
                   .map(energy_node)
                   .switch_latest()
                   )

#        discrete_streams = [input_R8.filter(oftype('engine/STEP'))]
#        discrete8 = rx.Observable.combine_latest()


        output8s = [energy8,]

        self._output8 = Observable.merge(output8s)

    @property
    def output8(self):
        return self._output8




def node(function, tag, scheduler=None):

    def inner(*args):
        incoming_seeds = [bm.seeds for bm in args]
        r_seeds = combine_seeds(*incoming_seeds)
        f_args = tuple([bm.payload for bm in args])

        def spawn_ex(e):
            return (rx.Observable
                    .just(error(tag=tag, ex=e, seeds=r_seeds))
                    )

        return (rx.Observable
                .from_(f_args, scheduler=scheduler)
                .map(function)
                .map(lambda value: ready(tag=tag, payload=value, seeds=r_seeds))
                .catch_exception(spawn_ex)
                )
    return inner


def ENERGY_node(bm):
    signals_array = bm.payload.data
    energy_array = compute_energy(signals_array)
    rbm = bm._replace(tag='engine/ENERGY', payload=energy_array)
    return rbm



def compute_energy(signals):
    signals_array = signals.data
    1/0
    return np.sum(signals_array **2, axis=0)

