# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:45:24 2017
@author: Jérémie Fache
"""

import rx
import time
from collections import namedtuple


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

buff_energy8 = energy8.buffer_with_count(1).map(lambda l: l[0])
#buff_energy8.subscribe(lambda x: print('{}'.format(x)))

def spawn_marker_pipeline(action):

    if action.tag == ADD:
        idx = action.payload
        idx8 = rx.Observable.just(idx)

        remove8 = action8.filter(lambda a: a.tag==REMOVE and a.payload==idx)
        removeall8 = action8.filter(lambda a: a.tag==REMOVE_ALL)
        cancel8 = rx.Observable.merge(remove8, removeall8)

        def select_e(i, data):
#            print('select {} in {}'.format(i, data))
            return data[i]

        e8 = (rx.Observable
              .combine_latest([idx8, buff_energy8], select_e)
              .map(lambda e: Msg('MARKER_{}_energy'.format(idx), e))
              )
        r8 = (rx.Observable
              .combine_latest([idx8, resource8], lambda i, rs: rs[i])
              .map(lambda e: Msg('MARKER_{}_resource'.format(idx), e))
              )


        return (rx.Observable
                .merge(e8, r8)
                .take_until(cancel8)
                )


energy = Accumulator('Energy')
resource = Accumulator('Resource')
pipeline8 = action8.flat_map(spawn_marker_pipeline)
pipeline8.subscribe(print)

action8.on_next(Msg(ADD, 2))
energy8.on_next(energy.get())
resource8.on_next(resource.get())

#energy8.on_next(energy.get())

action8.on_next(Msg(ADD, 3))
energy8.on_next(energy.get())




