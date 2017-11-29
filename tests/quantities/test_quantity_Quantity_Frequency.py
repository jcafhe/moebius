# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 10:19:27 2017

@author: Jérémie Fache
"""

import pytest
import moebius.quantity as qty


def test_Hz_to_kHz():
    f0 = qty.Frequency(1.25e3, 'Hz')
    f1 = f0.to('kHz')
    c = qty.Frequency(1.25, 'kHz')
    assert (f1.items == c.items)

def test_Hz_to_MHz():
    f0 = qty.Frequency(1.25e6, 'Hz')
    f1 = f0.to('MHz')
    c = qty.Frequency(1.25, 'MHz')
    assert (f1.items == c.items)

def test_Hz_to_GHz():
    f0 = qty.Frequency(1.25e9, 'Hz')
    f1 = f0.to('GHz')
    c = qty.Frequency(1.25, 'GHz')
    assert (f1.items == c.items)

# -----------------------------------------------------------------------------
def test_equal_Hz_vs_Hz():
    f0 = qty.Frequency(1.25, 'Hz')
    f1 = qty.Frequency(1.25, 'Hz')
    assert(f0 == f1)

def test_equal_Hz_vs_kHz():
    f0 = qty.Frequency(1250.0, 'Hz')
    f1 = qty.Frequency(1.25, 'kHz')
    assert(f0 == f1)

# -----------------------------------------------------------------------------
def test_Hz_add_Hz():
    f0 = qty.Frequency(2.0, 'Hz')
    f1 = qty.Frequency(3.0, 'Hz')
    fc = qty.Frequency(5.0, 'Hz')
    assert (fc == f0 + f1)

def test_Hz_add_kHz():
    f0 = qty.Frequency(200.0, 'Hz')
    f1 = qty.Frequency(3.0, 'kHz')
    fc = qty.Frequency(3.200, 'kHz')
    assert (fc == f0 + f1)

def test_kHz_add_Hz():
    f0 = qty.Frequency(200.0, 'Hz')
    f1 = qty.Frequency(3.0, 'kHz')
    fc = qty.Frequency(3.200, 'kHz')
    assert (fc == f1 + f0)

# -----------------------------------------------------------------------------
def test_Hz_sub_Hz():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Frequency(3.0, 'Hz')
    fc = qty.Frequency(2.0, 'Hz')
    assert (fc == f0 - f1)

def test_Hz_sub_kHz():
    f0 = qty.Frequency(5000.0, 'Hz')
    f1 = qty.Frequency(3.0, 'kHz')
    fc = qty.Frequency(2.0, 'kHz')
    assert (fc == f0 - f1)

def test_kHz_sub_Hz():
    f0 = qty.Frequency(5.0, 'kHz')
    f1 = qty.Frequency(3000.0, 'Hz')
    fc = qty.Frequency(2.0, 'kHz')
    assert (fc == f0 - f1)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def test_Hz_tdiv_Hz_return_Scalar():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 / f1
    fc = qty.Scalar(2.5)
    assert (fc == fr)

def test_Hz_tdiv_kHz_return_Scalar():
    f0 = qty.Frequency(5000.0, 'Hz')
    f1 = qty.Frequency(2.0, 'kHz')
    fr = f0 / f1
    fc = qty.Scalar(2.5)
    assert (fc == fr)

def test_kHz_tdiv_Hz_return_Scalar():
    f0 = qty.Frequency(5.0, 'kHz')
    f1 = qty.Frequency(2000.0, 'Hz')
    fr = f0 / f1
    fc = qty.Scalar(2.5)
    assert (fc == fr)

def test_Hz_tdiv_scalar_return_Hz():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Scalar(2.0)
    fr = f0 / f1
    fc = qty.Frequency(2.5, 'Hz')
    assert (fc == fr)

def test_Hz_tdiv_Undef_return_Undef():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Undefined(2.0)
    fr = f0 / f1
    fc = qty.Undefined(2.5)
    assert (fc == fr)

def test_scalar_tdiv_Hz_return_Undef():
    f0 = qty.Scalar(5.0)
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 / f1
    fc = qty.Undefined(2.5)
    assert (fc == fr)

def test_Undef_tdiv_Hz_return_Undef():
    f0 = qty.Undefined(5.0)
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 / f1
    fc = qty.Undefined(2.5)
    assert (fc == fr)

# -----------------------------------------------------------------------------
def test_Hz_fdiv_Hz_return_Scalar():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 // f1
    fc = qty.Scalar(2.0)
    assert (fc == fr)

def test_Hz_fdiv_kHz_return_Scalar():
    f0 = qty.Frequency(5000.0, 'Hz')
    f1 = qty.Frequency(2.0, 'kHz')
    fr = f0 // f1
    fc = qty.Scalar(2.0)
    assert (fc == fr)

def test_kHz_fdiv_Hz_return_Scalar():
    f0 = qty.Frequency(5.0, 'kHz')
    f1 = qty.Frequency(2000.0, 'Hz')
    fr = f0 // f1
    fc = qty.Scalar(2.0)
    assert (fc == fr)

def test_Hz_fdiv_scalar_return_Hz():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Scalar(2.0)
    fr = f0 // f1
    fc = qty.Frequency(2.0, 'Hz')
    assert (fc == fr)

def test_Hz_fdiv_Undef_return_Undef():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Undefined(2.0)
    fr = f0 // f1
    fc = qty.Undefined(2.0)
    assert (fc == fr)

def test_scalar_fdiv_Hz_return_Undef():
    f0 = qty.Scalar(5.0)
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 // f1
    fc = qty.Undefined(2.0)
    assert (fc == fr)

def test_Undef_fdiv_Hz_return_Undef():
    f0 = qty.Undefined(5.0)
    f1 = qty.Frequency(2.0, 'Hz')
    fr = f0 // f1
    fc = qty.Undefined(2.0)
    assert (fc == fr)


# -----------------------------------------------------------------------------
def test_Hz_mul_Hz_return_Undef():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Frequency(2.0, 'Hz')
    fc = qty.Undefined(10.0)
    fr = f0 * f1
    assert (fc == fr)


def test_Hz_mul_kHz_return_Undef():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Frequency(2.0, 'kHz')
    fc = qty.Undefined(10000.0)
    fr = f0 * f1
    assert (fc == fr)


def test_kHz_mul_Hz_return_Undef():
    f0 = qty.Frequency(5.0, 'kHz')
    f1 = qty.Frequency(2.0, 'Hz')
    fc = qty.Undefined(0.01)
    fr = f0 * f1
    assert (fc == fr)

def test_Hz_mul_Scalar_return_Hz():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Scalar(2.0)
    fc = qty.Frequency(10.0, 'Hz')
    fr = f0 * f1
    assert (fc == fr)

def test_Hz_mul_Undef_return_Undef():
    f0 = qty.Frequency(5.0, 'Hz')
    f1 = qty.Undefined(2.0)
    fc = qty.Undefined(10.0)
    fr = f0 * f1
    assert (fc == fr)
