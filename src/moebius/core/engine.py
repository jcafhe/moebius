# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:23:34 2017
@author: Jérémie Fache
"""

from collections import namedtuple
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
Shape = namedtuple('Shape', 'ordering, height, width')

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Engine():
    def __init__(self, busMessage8):
        main_scheduler = rx.concurrency.EventLoopScheduler()
        inputR8 = (busMessage8
                    .observe_on(main_scheduler)
                    .filter(oftype(status=READY))
                    )

        ascanR8 = inputR8.filter(oftype('ASCAN', READY))

        energy_node = node(function=compute_energy,
                           tag='ENERGY',
                           scheduler=rx.concurrency.thread_pool_scheduler)

        energy8 = (ascanR8
                   .map(energy_node)
                   .switch_latest()
                   )

        uv8 = uv(inputR8.filter(oftype('SHAPE', READY)))

        markers8 = markers(inputR8, inputR8.filter(oftype('SHAPE')))

        self._output8 = Observable.merge([energy8,
                                          markers8,
                                          uv8,
                                          ])



    @property
    def output8(self):
        return self._output8


## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
#def markers(action8, uv8):
#    tag = 'MARKERS'
#
#    def reducer(previous_bm, bm):
#        state = previous_bm.payload
#
#        if bm.tag == 'MARKER_ADD':
#            idx = int(bm.payload)
#            if idx < 0:
#                raise ValueError('MARKER_ADD does not support index < 0. '
#                                 'Got {}'.format(idx))
#            next_state = state.add(int(bm.payload))
#            return ready(tag=tag,
#                         payload=next_state,
#                         seeds=bm.seeds)
#
#        if bm.tag == 'MARKER_REMOVE':
#            next_state = state.remove(int(bm.payload))
#            return ready(tag=tag,
#                         payload=next_state,
#                         seeds=bm.seeds)
#
#        if bm.tag == 'MARKER_CLEAR_ALL':
#            next_state = ps()
#            return ready(tag=tag,
#                         payload=next_state,
#                         seeds=bm.seeds)
#
#        if bm.tag == 'MARKER_MOVE':
#            origin = bm.payload.origin
#            destination = bm.payload.destination
#            if origin < 0 or destination < 0:
#                etext = ('MARKER_MOVE does not support index < 0. '
#                         'Got origin:{} destination:{}'
#                         .format(origin, destination))
#                raise ValueError(etext)
#
#            next_state = state.remove(origin)
#            next_state = state.add(destination)
#
#            return ready(tag=tag,
#                         payload=next_state,
#                         seeds=bm.seeds)
#
#        return previous_bm
#        etext = 'Action not handled from message {}'.format(bm)
#        raise ValueError(etext)
#
#
#    reducer_tags = ['MARKER_ADD', 'MARKER_REMOVE', 'MARKER_CLEAR_ALL', 'MARKER_MOVE']
#    idx8 = (action8
#            .filter(oftype(tag=reducer_tags, status=READY))
#            .scan(reducer, seed=ready(tag=tag, payload=ps()))
#            )
#
#
#
#    move_up8 = action8.filter(oftype('MARKER_MOVE_UP', READY))
#    move_down8 = action8.filter(oftype('MARKER_MOVE_DOWN', READY))
#    move_left8 = action8.filter(oftype('MARKER_MOVE_LEFT', READY))
#    move_right8 = action8.filter(oftype('MARKER_MOVE_RIGHT', READY))

#    def translate():
#        pass


#    idx_trans8 = (rx.combine_latest())

#    def translate(indexes, shape):
#
#    pipeline8 = (rx.Observable.combine_latest(in8s))
    pipeline8 = rx.Observable.merge(idx8)
    return pipeline8


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def uv(shapeR8):
    tag = 'UV'

    def compute(shape):
        if shape.ordering == 'SNAKE':
            sh = (shape.height, shape.width)
            idxs = np.arange(sh[0] * sh[1]).reshape(sh)
            idxs[1::2] = np.flip(idxs[1::2], axis=1)
            return idxs

        raise NotImplementedError('UV only snake ordering implemented')

    def inner(bm):
        shape = bm.payload
        uv = compute(shape)
        return bm._replace(tag=tag, payload=uv)

    return (shapeR8.map(inner))


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
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


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def ENERGY_node(bm):
    signals_array = bm.payload.data
    energy_array = compute_energy(signals_array)
    rbm = bm._replace(tag='engine/ENERGY', payload=energy_array)
    return rbm



# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def compute_energy(signals):
    signals_array = signals
#    signals_array = signals.data
#    1/0
    return np.sum(signals_array **2, axis=0)

