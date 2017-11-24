# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:02:17 2017
@author: Jérémie Fache
"""
import numpy as np
import rx
from moebius.core import markers



def test_1():
    signals_0 = np.arange(10 * 6).reshape((10, 6))
    signals_1 = np.arange(10 * 6).reshape((10, 6)) + 100
    signals_2 = np.arange(10 * 6).reshape((10, 6)) + 1000


    mid = 'MID'
    scheduler = rx.testing.TestScheduler()
    extract_signal = markers.create_extract_signal(mid, scheduler)



