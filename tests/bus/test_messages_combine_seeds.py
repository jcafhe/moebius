# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:44:15 2017
@author: Jérémie Fache
"""

import pytest
from pyrsistent import (m as pm, s as ps, freeze)
from moebius.bus.messages import (ready, UNIDENTIFIED, NO_SEED, combine_seeds)



# -----------------------------------------------------------------------------
def test_combine_with_no_seeds():

    seeds = freeze({UNIDENTIFIED: ps()})

    bm0 = ready('BM0', None, seeds=NO_SEED)
    bm1 = ready('BM0', None, seeds=NO_SEED)
    result = combine_seeds(bm0.seeds, bm1.seeds)
    assert (result == seeds)



# -----------------------------------------------------------------------------
def test_combine_multiple_seeds():
    FOO = 'FOO'
    BAR = 'BAR'
    BAZ = 'BAZ'

    s0 = freeze({FOO: ps('#00'),
                 BAR: ps('#01'),
                 })

    s1 = freeze({ BAZ: ps('#02')
                })

    s2 = freeze({FOO: ps('#03'),
                 BAR: ps('#04'),
                 BAZ: ps('#05', '#06'),
                 })

    s3 = freeze({UNIDENTIFIED: ps(),
                 })

    expected = freeze({UNIDENTIFIED: ps(),
                       FOO: ps('#00', '#03'),
                       BAR: ps('#01', '#04'),
                       BAZ: ps('#02', '#05', '#06'),
                       })


    result = combine_seeds(s0, s1, s2, s3)
    assert (result == expected)

