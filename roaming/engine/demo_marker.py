# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 21:18:31 2017
@author: Jérémie Fache
"""

import rx
from moebius.sharereplay import share_replay
from moebius.bus.messages import (ready, oftype, READY)
from moebius.core import markers
import numpy as np

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


energy_data = Accumulator('eny')
action8 = rx.subjects.Subject()

push_signal = rx.subjects.Subject()
push_energy = rx.subjects.Subject()
push_sr = rx.subjects.Subject()

signalsR8 = push_signal
energyR8 = push_energy
srR8 = push_sr

pipeline8 = markers.create_markers_pipeline(action8,
                                            signalsR8=signalsR8,
                                            energiesR8=energyR8,
                                            sampling_rateR8=srR8)

ids = ['ID#{:02}'.format(i) for i in range(20)]

print('\nSTARTING ...')
signalsR8.subscribe(print)
energyR8.subscribe(print)
pipeline8.subscribe(print)

print('\ntrack ID#00')
action8.on_next(markers.track(ids[0]))

print('\ntrack ID#01')
action8.on_next(markers.track(ids[1]))

print('\ntrack ID#02')
action8.on_next(markers.track(ids[2]))


print('\nupdate #01 with sig_idx=2')
action8.on_next(markers.update_signal_idx('ID#01', 2))

print('\npushing sr')
push_sr.on_next(ready('SAMPLING_RATE', 20))

print('\npushing signals')
push_signal.on_next(ready('SIGNALS', np.arange(6*3).reshape((6,3)) + 10))

print('\nupdate #00 with sig_idx=0')
action8.on_next(markers.update_signal_idx(ids[0], 0))

print('\nupdate #02 with sig_idx=2')
action8.on_next(markers.update_signal_idx(ids[2], 2))

print('\nuntrack #01')
action8.on_next(markers.untrack(ids[1]))

print('\npushing signals')
push_signal.on_next(ready('SIGNALS', np.arange(6*3).reshape((6,3)) + 20))
