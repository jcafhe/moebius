# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:15:10 2017
@author: Jérémie Fache
"""
import logging
log_format = '%(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
import numpy as np
from collections import namedtuple
import rx
logging.getLogger('Rx').setLevel(logging.CRITICAL)
from feedback import scan_map

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
energyR8 = rx.subjects.Subject()

# -----------------------------------------------------------------------------
def markers_reducer(stateR, actionR):
    print('execute markers_reducer with {} {}'.format(stateR, actionR))
    state = stateR.payload
    tag = 'MARKERS'

    if stateR.tag == DEFAULT:
        return Msg(tag, ps())

    if actionR.tag == ADD:
        state = state.add(actionR.payload)
        return Msg(tag, state)

    if actionR.tag == REMOVE:
        state = state.remove(actionR.payload)
        return Msg(tag, state)

    if actionR.tag == REMOVE_ALL:
        state = ps()
        return Msg(tag, state)

    return Msg(tag, state)


# -----------------------------------------------------------------------------
def marker_energy(markersR8, energyR8):

    def combine(markersR, energyR):
        return pm(markersR=markersR,
                  energyR=energyR)

    def serialize_by_marker(d):
        markers = d.markersR.payload
        energy = d.energyR.payload
        # TODO combine seeds
        li = [pm(marker=marker, energy=energy) for marker in markers]
        return rx.Observable.from_(li)

    def key_selector(d):
        return d.marker

    def duration_selector(group):
        key = group.key
#        print('\tdefining duration of group[{}]'.format(key))

        def filt(mksR):
            mks = mksR.payload
#            print('\t\t{}\t{}'.format(mksR, id(mksR)))
#            print('\t\ttesting key[{}] in markers:{}'.format(key, mks))
            return key not in mks

        killer8 = (markersR8
                   .filter(filt)
                   )
        return killer8

    def group_pipeline(group):

        key = group.key
#        print('\tcreating group[{}]'.format(key))
        def compare(last, new):
            return last is new

        return (group
                .distinct_until_changed(lambda d: d.energy, compare)
#                .do_action(lambda x : print('debug group[{}] {}'.format(group.key, id(x.energy))))
                .map(lambda d: d.energy[key])
                .map(lambda e: Msg('MARKER_{}_ENERGY'.format(key), e))
                )


    pipeline8 = (rx.Observable
                 .combine_latest(markersR8, energyR8, combine)
                 .switch_map(serialize_by_marker)
                 .group_by_until(key_selector=key_selector,
                                 element_selector=None,
                                 duration_selector=duration_selector)
                 .map(group_pipeline)
                 .merge_all()
                 )
    return pipeline8


# -----------------------------------------------------------------------------
markersR8 = (actionR8
             .scan(markers_reducer, seed=Msg(DEFAULT, None))
#             .share()
             )
marker_energyM8 = marker_energy(markersR8, energyR8)


markersR8.subscribe(lambda m: print('{}\t{}'.format(m, id(m))))
marker_energyM8.subscribe(lambda m: print('{}'.format(m)))

#print('==============================')
#print('adding markers 0, 3, 5')
#actionR8.on_next(Msg(ADD, 0))
#actionR8.on_next(Msg(ADD, 3))
#actionR8.on_next(Msg(ADD, 5))
#print('==============================')
#print('pushing energy0')
#energyR8.on_next(Msg(ENERGY, energy_data.get()))
#
#print('==============================')
#print('removing all markers')
#actionR8.on_next(Msg(REMOVE_ALL, None))
#print('==============================')
#print('pushing energy1')
#energyR8.on_next(Msg(ENERGY, energy_data.get()))
print('==============================')
print('pushing energy2')
energyR8.on_next(Msg(ENERGY, energy_data.get()))

print('==============================')
print('adding markers 0, 3, 5, 6')
print('\nadding 0 :::::::::::::::::::::')
actionR8.on_next(Msg(ADD, 0))
print('\nadding 3 :::::::::::::::::::::')
actionR8.on_next(Msg(ADD, 3))
print('\nadding 5 :::::::::::::::::::::')
actionR8.on_next(Msg(ADD, 5))
print('\nadding 6 :::::::::::::::::::::')
actionR8.on_next(Msg(ADD, 6))
print('\nadding 7 :::::::::::::::::::::')
actionR8.on_next(Msg(ADD, 7))
print('==============================')
print('removing markers 0, 3')
actionR8.on_next(Msg(REMOVE, 0))
actionR8.on_next(Msg(REMOVE, 3))

print('==============================')
print('pushing energy3')
energyR8.on_next(Msg(ENERGY, energy_data.get()))



