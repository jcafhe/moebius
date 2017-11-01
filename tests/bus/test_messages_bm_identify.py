# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 13:30:10 2017

@author: Jérémie Fache
"""

import pytest
from pyrsistent import (PMap, m, PVector, v, s, PSet, freeze)

from moebius.bus import messages




def test_identify_with_alphanumeric_tag():
    uid = 'UID'
    tag = 'a_tag_0'
    status = 'a_status_0'

    m0 = messages.BusMessage(tag=tag, status=status, payload=0, seeds=m())
    m1 = m0.identify(uid)

    seeds_c = freeze({tag:s(uid)})
    mc = messages.BusMessage(tag=tag, status=status, payload=0, seeds=seeds_c)
    assert(m1 == mc)


def test_identify_with_non_alphanumeric_tag_status():
    uid = 'UID'
    tag = 'a tag #0'
    status = 'a status #0'

    m0 = messages.BusMessage(tag=tag, status=status, payload=0, seeds=m())
    m1 = m0.identify(uid)

    seeds_c = freeze({tag:s(uid)})
    mc = messages.BusMessage(tag=tag, status=status, payload=0, seeds=seeds_c)
    assert(m1 == mc)

def test_identify_with_non_alphanumeric_tag_status_uid():
    uid = 'UID %-'
    tag = 'a tag #0'
    status = 'a status #0'

    m0 = messages.BusMessage(tag=tag, status=status, payload=0, seeds=m())
    m1 = m0.identify(uid)

    seeds_c = freeze({tag:s(uid)})
    mc = messages.BusMessage(tag=tag, status=status, payload=0, seeds=seeds_c)
    assert(m1 == mc)

