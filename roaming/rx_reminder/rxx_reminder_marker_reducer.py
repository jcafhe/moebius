# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:08:59 2017
@author: Jérémie Fache
"""

import rx
import time
from collections import namedtuple
from pyrsistent import (s as ps, v as pv, m as pm)

State = namedtuple('State', 'content, output')



class Accumulator():
    items_count = 6

    def __init__(self, name):
        self._name = name
        self._count = 0

    def get(self):
        name = self._name
        count = self._count
        items_count = self.items_count
        data = ['[{}_{}] {}'.format(name, count, i) for i in range(items_count)]
        self._count += 1
        return data


Msg = namedtuple('Msg', 'tag, payload')
ADD = 'ADD'
REMOVE = 'REMOVE'
REMOVE_ALL = 'REMOVE_ALL'
ENERGY = 'ENERGY'

action8 = rx.subjects.Subject()
energy8 = rx.subjects.Subject()
resource8 = rx.subjects.Subject()


def marker_node(action8):
    class Anonymous():
        pass
    NO_OUTPUT = Anonymous()

    def marker_reducer(state, action):
        last_markers = state.content

        if action.tag == 'ADD':
            idx = action.payload
            markers = last_markers.add(idx)
            diff = ps(idx)

            content = markers
            output = action._replace(tag='MARKERS',
                                     payload=pm(all=markers, diff=diff))
            return State(content=content, output=output)

        if action.tag == 'REMOVE':
            idx = action.payload
            markers = last_markers.remove(idx)
            diff = ps()

            content = markers
            output = action._replace(tag='MARKERS',
                                     payload=pm(all=markers, diff=diff))
            return State(content=content, output=output)

        if action.tag == 'REMOVE_ALL':

            markers = ps()
            diff = ps()

            content = markers
            output = action._replace(tag='MARKERS',
                                     payload=pm(all=markers, diff=diff))
            return State(content=content, output=output)

        return state._replace(output=NO_OUTPUT)

    return (action8
            .scan(marker_reducer, seed=State(content=ps(), output=NO_OUTPUT))
            .map(lambda st: st.output)
            .filter(lambda out: out is not NO_OUTPUT)
            )


def energy_marker_node(markers8, energy8):

#    diff8 = (markers8
#             .map(lambda m: m.payload.diff)
#             .filter(lambda mks: len(mks.diff)) > 0)
#             .map(lambda mks: rx.Observable.from_(mks))
#             )
#    def reducer(state, message):
#        if message.tag == ''
        #        if

    def serialize(d):
        # d = pmap {markers_msg: ps(...), energy_msg: [...] }
        markers= d.markers_msg.payload.all
        energy = d.energy_msg.payload
        li = [pm(index=idx, energy=energy) for idx in markers]
        return rx.Observable.from_(li)

    def group_pipeline(obs):
        # d = pmap {index: int, energy: [...] }
        return (obs
                .distinct_until_changed(lambda d: d.energy, lambda old, new: old is new)
                .map(lambda d: Msg('MARKER_{}_ENERGY'.format(d.index), d.energy[d.index]))
                )

    pipeline = (rx.Observable
                .combine_latest(markers8, energy8, lambda mks, e: pm(markers_msg=mks, energy_msg=e))
                .flat_map(serialize)
                .group_by(lambda d: d.index)
                .flat_map(group_pipeline)
                )

    return pipeline

#def energy_reducer(state, message):
#    last_markers = state.content
#
#    if message.tag == 'MARKERS':
#        markers = message.payload
#        diff_markers = []
#        for marker in markers:
#            if not marker in last_markers:
#                diff_markers.append(marker)
#
#            next_state=State(content=markers, output=diff_markers)
#            return next_state
#
#    if message.tag == 'ENERGY':
#        next_state = State(content=last_markers, output=last_markers)
#        return next_state
#
#    return State(content=last_markers, output=[])
#
#marker_energy8 = (rx.Observable
#                  .merge(action8, energy8)
#                  .scan(energy_reducer)
#                  )

create_energy = Accumulator('energy')

markers8 = marker_node(action8)
marker_energy8 = energy_marker_node(markers8, energy8)
markers8.subscribe(print)
marker_energy8.subscribe(print)

energy8.on_next(Msg(ENERGY, create_energy.get()))
action8.on_next(Msg(ADD, 3))
action8.on_next(Msg(ADD, 5))
action8.on_next(Msg(ADD, 1))
print('======================================')
#action8.on_next(Msg(REMOVE, 3))
print('new energy')
energy8.on_next(Msg(ENERGY, create_energy.get()))
action8.on_next(Msg(REMOVE_ALL, None))
energy8.on_next(Msg(ENERGY, create_energy.get()))
energy8.on_next(Msg(ENERGY, create_energy.get()))
print('======================================')
action8.on_next(Msg(ADD, 3))



