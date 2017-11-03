# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 15:00:05 2017
@author: Jérémie Fache
"""
import pytest
from pyrsistent import (m as pm, s as ps, freeze)
from moebius.bus import messages


def test_ready_message():
    tag = 'tag%'
    seeds = freeze({'seed0%': ps('id#0'),
                    'seed1%': ps('id1#') })

    status = messages.READY
    payload = 'payload%'

    bm_r = messages.ready(tag=tag, payload=payload, seeds=seeds)
    assert (bm_r.tag == tag)
    assert (bm_r.seeds == seeds)
    assert (bm_r.status == status)
    assert (bm_r.payload == payload)


def test_processing_message():
    tag = 'tag%'
    seeds = freeze({'seed0%': ps('id#0'),
                    'seed1%': ps('id1#') })

    status = messages.PROCESSING
    ratio = (1, 10)
    meta = 'meta%'

    bm_r = messages.processing(tag=tag, ratio=ratio, meta=meta, seeds=seeds)
    assert(bm_r.tag == tag)
    assert(bm_r.seeds == seeds)
    assert(bm_r.status == status)
    assert(bm_r.payload.ratio == ratio)
    assert(bm_r.payload.meta == meta)
