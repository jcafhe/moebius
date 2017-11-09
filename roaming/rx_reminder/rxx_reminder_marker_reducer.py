# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 19:08:59 2017
@author: Jérémie Fache
"""

import rx
import time
from collections import namedtuple


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

action8 = rx.subjects.Subject()
energy8 = rx.subjects.Subject()
resource8 = rx.subjects.Subject()



def energy_reducer(state, message):
    last_markers = state.content

    if message.tag == 'MARKERS':
        markers = message.payload
        diff_markers = []
        for marker in markers:
            if not marker in last_markers:
                diff_markers.append(marker)

            next_state=State(content=markers, output=diff_markers)
            return next_state

    if message.tag == 'ENERGY':
        next_state = State(content=last_markers, output=last_markers)
        return next_state

    return State(content=last_markers, output=[])

marker_energy8 = (rx.Observable
                  .merge(action8, energy8)
                  .scan(energy_reducer)
                  )





