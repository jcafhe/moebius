# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:23:34 2017
@author: Jérémie Fache
"""
import numpy as np
import rx
from pyrsistent import (s as ps)
from rx import Observable
from moebius.bus.messages import (BM, READY, ready, error, oftype, combine_seeds)
from . import api


"""
input:
ASCAN np.array 2d


output:
ENERGY np.array 1d
MARKED_IDXS tuple
MARKER_FFT

"""


class Engine():
    def __init__(self, busMessage8):
        main_scheduler = rx.concurrency.EventLoopScheduler()
        input_R8 = (busMessage8
                    .observe_on(main_scheduler)
                    .filter(oftype(status=READY))
                    )

        ascanR8 = input_R8.filter(oftype('ASCAN', READY))

        energy_node = node(function=compute_energy,
                           tag='ENERGY',
                           scheduler=rx.concurrency.thread_pool_scheduler)

        energy8 = (ascanR8
                   .map(energy_node)
                   .switch_latest()
                   )

        markers8 = markers(input_R8)

        self._output8 = Observable.merge([energy8,
                                          markers8,
                                          ])

    @property
    def output8(self):
        return self._output8


def markers(bm8):
    tag = 'MARKERS'

    def reducer(previous_bm, bm):
        state = previous_bm.payload

        if bm.tag == 'MARKER_ADD':
            next_state = state.add(int(bm.payload))
            return ready(tag=tag,
                         payload=next_state,
                         seeds=bm.seeds)

        if bm.tag == 'MARKER_REMOVE':
            next_state = state.remove(int(bm.payload))
            return ready(tag=tag,
                         payload=next_state,
                         seeds=bm.seeds)

        if bm.tag == 'MARKER_CLEAR_ALL':
            next_state = ps()
            return ready(tag=tag,
                         payload=next_state,
                         seeds=bm.seeds)

        etext = 'Action not handled from message {}'.format(bm)
        raise ValueError(etext)

    pipeline = (bm8
                .filter(oftype(tag='MARKER...', status=READY))
                .scan(reducer, seed=ready(tag=tag, payload=ps()))
               )

    return pipeline


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
    signals_array = signals
#    signals_array = signals.data
#    1/0
    return np.sum(signals_array **2, axis=0)

