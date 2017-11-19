# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:46:03 2017
@author: Jérémie Fache
"""

from collections import namedtuple

import numpy as np
import rx
import sharereplay
from pyrsistent import(m as pm,
                       s as ps,
                       v as pv,
                       freeze)


class Accumulator():
    items_count = 10

    def __init__(self, name):
        self._name = name
        self._count = 0

    def get(self):
        name = self._name
        count = self._count
        items_count = self.items_count
        data = ['[{}_{}] {}'.format(name, count, i) for i in range(items_count)]
        self._count += 1
        data = np.array(data)
        return data

print('STARTING ...')

Msg = namedtuple('Msg', 'tag, payload')
ADD = 'ADD'
REMOVE = 'REMOVE'
REMOVE_ALL = 'REMOVE_ALL'
ENERGY = 'ENERGY'
DEFAULT = 'DEFAULT'

energy_data = Accumulator('eny')
actionR8 = rx.subjects.Subject()
push_energy = rx.subjects.Subject()

energyR8 = push_energy.share_replay(1)

addR8 = actionR8.filter(lambda m: m.tag==ADD)
remR8 = actionR8.filter(lambda m: m.tag==REMOVE)
remallR8 =  actionR8.filter(lambda m: m.tag==REMOVE_ALL)


# -----------------------------------------------------------------------------
def spawn_marker_pipeline(addR):
    index = addR.payload

    killer8 = (remR8
               .filter(lambda m: m.payload == index)
               )

    return (energyR8
            .take_until(killer8)
            .map(lambda m: m.payload[index])
            .map(lambda e: Msg('MARKER_ENERGY_{}'.format(index), e))
            )

# -----------------------------------------------------------------------------


markerR8 = (addR8
            .flat_map(spawn_marker_pipeline)
            )

markerR8.subscribe(print)

print('adding 0')
actionR8.on_next(Msg(ADD, 0))
print('adding 1')
actionR8.on_next(Msg(ADD, 1))

print('pushing energy 0')
push_energy.on_next(Msg(ENERGY, energy_data.get()))

print('pushing energy 1')
push_energy.on_next(Msg(ENERGY, energy_data.get()))

print('adding 5')
actionR8.on_next(Msg(ADD, 5))

print('removing 1')
actionR8.on_next(Msg(REMOVE, 1))

print('pushing energy 2')
push_energy.on_next(Msg(ENERGY, energy_data.get()))








