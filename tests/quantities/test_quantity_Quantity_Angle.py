# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 14:29:36 2017

@author: Jérémie Fache
"""

import pytest
import math
from moebius.quantity import (Scalar, Undefined, Angle)


def test_to__deg_rad():
    a = Angle(3.0, '°')
    c = Angle(math.radians(3.0), 'rad')
    assert (abs(c - a) < c.update(value=c.value * 1.0e-10))



def test_to__rad_deg():
    a = Angle(3.0, 'rad')
    c = Angle(math.degrees(3.0), '°')
    assert (abs(c - a) < c.update(value=c.value * 1.0e-10))

