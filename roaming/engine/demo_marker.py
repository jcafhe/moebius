# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:03:34 2017
@author: Jérémie Fache
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 21:18:31 2017
@author: Jérémie Fache
"""

import rx
from moebius.sharereplay import share_replay
from moebius.bus.messages import (ready, oftype, READY)
from moebius.core import markers2
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

mids = ['ID{:1}'.format(i) for i in range(5)]

pipeline8 = markers2.create_markers(marker_ids=mids,
                                    action8=action8,
                                    signalsR8=signalsR8,
                                    energiesR8=energyR8,
                                    sampling_rateR8=srR8)


print('\nSTARTING ...')
signalsR8.subscribe(print)
energyR8.subscribe(print)
pipeline8.subscribe(print)

print('\nenable all markers')
for mid in mids:
    action8.on_next(markers2.bm_status(mid, markers2.ENABLE))


print('update 0 with sig_idx=0')
action8.on_next(markers2.bm_signal_idx(mids[0], 0))
print('update 01 with sig_idx=1')
action8.on_next(markers2.bm_signal_idx(mids[1], 1))
print('update 02 with sig_idx=2')
action8.on_next(markers2.bm_signal_idx(mids[2], 2))

print('\npushing sr = 20Hz')
push_sr.on_next(ready('SAMPLING_RATE', 20))

print('\npushing signals and energies')
sigs = np.arange(6*3).reshape((6,3))
enes = np.sum(sigs, axis=1)
push_signal.on_next(ready('SIGNALS', sigs))
push_energy.on_next(ready('ENERGIES', enes))

print('\ndisable marker 01')
action8.on_next(markers2.bm_status(mids[1], markers2.DISABLE))

print('\npushing signals and energies')
sigs = np.arange(6*3).reshape((6,3)) + 10
enes = np.sum(sigs, axis=1)
push_signal.on_next(ready('SIGNALS', sigs))
push_energy.on_next(ready('ENERGIES', enes))


print('\nreenable marker 01')
action8.on_next(markers2.bm_status(mids[1], markers2.ENABLE))

print('\nupdate #00 with sig_idx=0')
action8.on_next(markers2.bm_signal_idx(mids[0], 3))
#
#print('\nupdate #02 with sig_idx=2')
#action8.on_next(markers2.update_signal_idx(ids[2], 2))
#
#print('\nuntrack #01')
#action8.on_next(markers2.untrack(ids[1]))
#
#print('\npushing signals')
#push_signal.on_next(ready('SIGNALS', np.arange(6*3).reshape((6,3)) + 20))
