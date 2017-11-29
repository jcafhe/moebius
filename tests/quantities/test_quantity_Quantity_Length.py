# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 13:40:43 2017

@author: Jérémie Fache
"""

import pytest
from moebius.quantity import (Scalar, Undefined, Length)



def test_Length_to__m_mm():
    l = Length(3.0, 'm')
    c = Length(3000.0, 'mm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__mm_m():
    l = Length(3.0, 'mm')
    c = Length(0.003, 'm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))

def test_Length_to__m_µm():
    l = Length(3.0, 'm')
    c = Length(3.0e6, 'µm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__µm_m():
    l = Length(3.0, 'µm')
    c = Length(3.0e-6, 'm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__m_nm():
    l = Length(1.0, 'm')
    c = Length(1.0e9, 'nm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__nm_m():
    l = Length(3.0e9, 'nm')
    c = Length(3.0, 'm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__m_pm():
    l = Length(3.0, 'm')
    c = Length(3.0e12, 'pm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__pm_m():
    l = Length(3000000000000, 'pm')
    c = Length(3, 'm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__µm_mm():
    l = Length(3.0, 'µm')
    c = Length(3.0e-3, 'mm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))


def test_Length_to__pm_mm():
    l = Length(3.0, 'pm')
    c = Length(3.0e-9, 'mm')
    assert (abs(c - l) < c.update(value=c.value * 1.0e-10))



