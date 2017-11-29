# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:15:55 2017
@author: Jérémie Fache
"""
import numpy as np


def assert_message_equality_with_np(bm0, bm1):
    assert(bm0.tag == bm1.tag)
    payload0 = bm0.payload
    payload1 = bm1.payload
    if isinstance(payload0, np.ndarray):
        if isinstance(payload1, np.ndarray):
            assert(np.all(payload0 == payload1))
        else:
            AssertionError('{} != {}'.format(payload0, payload1))
    else:
        if isinstance(payload1, np.ndarray):
            AssertionError('{} != {}'.format(payload0, payload1))
        assert(payload0 == payload1)

    assert(bm0.status == bm1.status)
    assert(bm0.seeds == bm1.seeds)
