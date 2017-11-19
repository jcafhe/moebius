# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:08:09 2017
@author: Jérémie Fache
"""
from collections import namedtuple
import rx
from pyrsistent import (m as pm, s as ps, v as pv)

Msg = namedtuple('Msg', 'tag, payload')
ADD = 'ADD'
REMOVE = 'REMOVE'
REMOVE_ALL = 'REMOVE_ALL'
ENERGY = 'ENERGY'

class _Unique:
    pass

INIT = _Unique()

action8 = rx.subjects.Subject()

# -----------------------------------------------------------------------------
def markers_reducer(stateR, actionR):
    print('execute markers_reducer with {} {}'.format(stateR, actionR))
    tag = 'MARKERS'

    if stateR is INIT:
        return Msg(tag, pv())

    state = stateR.payload

    if actionR.tag == ADD:
        state = state.append(actionR.payload)
        return Msg(tag, state)

    if actionR.tag == REMOVE:
        state = state.remove(actionR.payload)
        return Msg(tag, state)

    if actionR.tag == REMOVE_ALL:
        state = pv()
        return Msg(tag, state)

    return Msg(tag, state)

pipeline = (action8
            .scan(markers_reducer,seed=INIT)
#            .share()
            )

out_A = pipeline.subscribe(lambda m: print('out_A:: {}\tid: {}'.format(m, id(m))))
out_B = pipeline.subscribe(lambda m: print('out_B:: {}\tid: {}'.format(m, id(m))))


print('adding 0')
action8.on_next(Msg(ADD, 0))
print('adding 1')
action8.on_next(Msg(ADD, 1))
print('adding 2')
action8.on_next(Msg(ADD, 2))
print('subscribing with out_C')
out_C = pipeline.subscribe(lambda m: print('out_C:: {}\tid: {}'.format(m, id(m))))
print('adding 3')
action8.on_next(Msg(ADD, 3))
print('removing all')
#action8.on_next(Msg(REMOVE_ALL, 3))



