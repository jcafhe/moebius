# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 09:15:45 2017

@author: Jérémie Fache
"""

from moebius.quantity import Quantity

UNITS = ('u', 'ku')
Q_TAG = ('q_tag')
P_TAG = ('p_tag')
Q_SYMBOL = 'q_symbol'
P_SYMBOL = 'q_symbol'

# -----------------------------------------------------------------------------
class Q(Quantity):
    _UNITS = UNITS
    _FACTORS = {'u': 1.0, 'ku': 1000.0}

    @staticmethod
    def __units__():
        return Q._UNITS

    @staticmethod
    def __tag__():
        return Q_TAG

    @staticmethod
    def __symbol__():
        return Q_SYMBOL

    def __init__(self, v, u='u'):
        Quantity.__init__(self, v, u, self._UNITS)

    def to(self, unit):
        if unit == self.unit:
            return self
        f = self._FACTORS[self.unit] / self._FACTORS[unit]
        return Q(self.value * f, unit)



# -----------------------------------------------------------------------------
class P(Quantity):
    _UNITS = UNITS
    _FACTORS = {'u': 1.0, 'ku': 1000.0}

    @staticmethod
    def __units__():
        return P._UNITS

    @staticmethod
    def __tag__():
        return P_TAG

    @staticmethod
    def __symbol__():
        return P_SYMBOL

    def __init__(self, v, u='u'):
        Quantity.__init__(self, v, u, self._UNITS)

    def to(self, unit):
        if unit == self.unit:
            return self
        f = self._FACTORS[self.unit] / self._FACTORS[unit]
        return Q(self.value * f, unit)