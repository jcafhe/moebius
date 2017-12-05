# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 09:10:41 2017

@author: Jérémie Fache
"""
import numpy as np
import pytest
import moebius.quantity as qty
from .test_custom_quantities import (P, Q,
                                    UNITS,
                                    P_TAG, Q_TAG,
                                    P_SYMBOL, Q_SYMBOL)

# -----------------------------------------------------------------------------
def test_value():
    q = Q(12.0, 'u')
    r = q.value
    c = 12
    assert(c == r)


# -----------------------------------------------------------------------------
def test_unit():
    q = Q(12.0, 'u')
    r = q.unit
    c = 'u'
    assert(c == r)


# -----------------------------------------------------------------------------
def test_units_from_instance():
    q = Q(12.0, 'u')
    r = q.units
    c = UNITS
    assert(c == r)

def test_units_from_class():
    r = Q.units
    c = UNITS
    assert(c == r)

# -----------------------------------------------------------------------------
def test_tag_from_instance():
    q= Q(12.0, 'u')
    r = q.tag
    c = Q_TAG
    assert(c == r)

def test_tag_from_class():
    r = Q.tag
    c = Q_TAG
    assert(c == r)

# -----------------------------------------------------------------------------
def test_symbol_from_instance():
    q= Q(12.0, 'u')
    r = q.symbol
    c = Q_SYMBOL
    assert(c == r)

def test_symbol_from_class():
    r = Q.symbol
    c = Q_SYMBOL
    assert(c == r)


# -----------------------------------------------------------------------------
def test_getitem():
    q = Q(12.0, 'u')
    assert(12.0 == q['u'])


def test_getitem__with_implicit_conversion():
    q = Q(1200.0, 'u')
    assert(1.2 == q['ku'])


def test_getitem__wrong_unit_raises_KeyError():
    q = Q(1200.0, 'u')
    with pytest.raises(KeyError):
        q['eraeazfds']


# -----------------------------------------------------------------------------
def test_auto_positive_0():
    q = Q(1200.0, 'u')
    r = q.auto
    c = Q(1.2, 'ku')
    assert(c == r)


def test_auto_positive_1():
    q = Q(3.6e-6, 'ku')
    r = q.auto
    c = Q(3.6e-3, 'u')
    assert(c == r)


def test_auto_negative_0():
    q = Q(-1200.0, 'u')
    r = q.auto
    c = Q(-1.2, 'ku')
    assert(c == r)


def test_auto_negative_1():
    q = Q(-3.6e-6, 'ku')
    r = q.auto
    c = Q(-3.6e-3, 'u')
    assert(c == r)


def test_auto_zero():
    q = Q(0.0, 'u')
    r = q.auto
    c = Q(0.0, 'u')
    assert(c == r)


# -----------------------------------------------------------------------------
def test_equality__Qu_Qu():
    q0 = Q(12)
    q1 = Q(12)
    assert(q0 == q1)


def test_equality__Qu_Qv():
    q0 = Q(1200.0, 'u')
    q1 = Q(1.2, 'ku')
    assert(q0 == q1)


def test_equality__Q_S():
    q = Q(1200.0)
    s = qty.Scalar(1200.0)
    assert(q != s)


def test_equality__Q_U():
    q = Q(1200.0)
    u = qty.Undefined(1200.0)
    assert(q != u)


def test_equality__S_Q():
    q = Q(1200.0)
    s = qty.Scalar(1200.0)
    assert(s != q)


def test_equality__U_Q():
    q = Q(1200.0)
    u = qty.Undefined(1200.0)
    assert(u != q)


def test_equality__S_S():
    s0 = qty.Scalar(12.0)
    s1 = qty.Scalar(12.0)
    assert(s0 == s1)


def test_equality__U_U():
    u0 = qty.Undefined(12.0)
    u1 = qty.Undefined(12.0)
    assert(u0 == u1)

# -----------------------------------------------------------------------------
def test_equality__npQu_npQu():
    q0 = Q(np.arange(10))
    q1 = Q(np.arange(10))
    assert(q0 == q1)

def test_equality__npQu_Qu():
    q0 = Q(np.arange(10))
    q1 = Q(10)
    assert(q0 != q1)

def test_equality__Qu_npQu():
    q0 = Q(10)
    q1 = Q(np.arange(10))
    assert(q0 != q1)

def test_equality__npQu_npQv():
    q0 = Q(np.arange(10.0) * 1000.0, 'u')
    q1 = Q(np.arange(10.0), 'ku')
    assert(q0 == q1)


def test_equality__npQ_npS():
    q = Q(np.arange(10.0))
    s = qty.Scalar(np.arange(10.0))
    assert(q != s)


def test_equality__npQ_npU():
    q = Q(np.arange(10.0))
    u = qty.Undefined(np.arange(10.0))
    assert(q != u)


def test_equality__npS_npQ():
    q = Q(np.arange(10.0))
    s = qty.Scalar(np.arange(10.0))
    assert(s != q)


def test_equality__npU_npQ():
    q = Q(np.arange(10.0))
    u = qty.Undefined(np.arange(10.0))
    assert(u != q)


def test_equality__npS_npS():
    s0 = qty.Scalar(np.arange(10.0))
    s1 = qty.Scalar(np.arange(10.0))
    assert(s0 == s1)


def test_equality__npU_npU():
    u0 = qty.Undefined(np.arange(10.0))
    u1 = qty.Undefined(np.arange(10.0))
    assert(u0 == u1)


# -----------------------------------------------------------------------------
def test_gt__Qu_Qu():
    q0 = Q(12)
    q1 = Q(10)
    q2 = Q(14)
    assert(q0 > q1)
    assert(not q0 > q2)


def test_gt__Qu_Qv():
    q0 = Q(1200.0, 'u')
    q1 = Q(1.0, 'ku')
    q2 = Q(1.4, 'ku')
    assert(q0 > q1)
    assert(not q0 > q2)


def test_gt__S_S():
    s0 = qty.Scalar(12.0)
    s1 = qty.Scalar(10.0)
    s2 = qty.Scalar(14.0)
    assert(s0 > s1)
    assert(not s0 > s2)


def test_gt__U_U():
    u0 = qty.Undefined(12.0)
    u1 = qty.Undefined(10.0)
    u2 = qty.Undefined(14.0)
    assert(u0 > u1)
    assert(not u0 > u2)


def test_gt__Q_S_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        s = qty.Scalar(1200.0)
        q > s


def test_gt__Q_U_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        u = qty.Undefined(1200.0)
        q > u


def test_gt__S_Q_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        s = qty.Scalar(1200.0)
        s > q


def test_gt__S_U_raise_TypeError():
    with pytest.raises(TypeError):
        s = qty.Scalar(1200.0)
        u = qty.Undefined(1200.0)
        s > u


def test_gt__U_Q_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        u = qty.Undefined(1200.0)
        u > q


def test_gt__U_S_raise_TypeError():
    with pytest.raises(TypeError):
        u = qty.Undefined(1200.0)
        s = qty.Scalar(1200.0)
        u > s


# -----------------------------------------------------------------------------
def test_lt__Qu_Qu():
    q0 = Q(12)
    q1 = Q(14)
    q2 = Q(10)
    assert(q0 < q1)
    assert(not q0 < q2)


def test_lt__Qu_Qv():
    q0 = Q(1200.0, 'u')
    q1 = Q(1.4, 'ku')
    q2 = Q(1.0, 'ku')
    assert(q0 < q1)
    assert(not q0 < q2)


def test_lt__S_S():
    s0 = qty.Scalar(12.0)
    s1 = qty.Scalar(14.0)
    s2 = qty.Scalar(10.0)
    assert(s0 < s1)
    assert(not s0 < s2)


def test_lt__U_U():
    u0 = qty.Undefined(12.0)
    u1 = qty.Undefined(14.0)
    u2 = qty.Undefined(10.0)
    assert(u0 < u1)
    assert(not u0 < u2)


def test_lt__Q_S_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        s = qty.Scalar(1200.0)
        q < s


def test_lt__Q_U_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        u = qty.Undefined(1200.0)
        q < u


def test_lt__S_Q_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        s = qty.Scalar(1200.0)
        s < q


def test_lt__S_U_raise_TypeError():
    with pytest.raises(TypeError):
        s = qty.Scalar(1200.0)
        u = qty.Undefined(1200.0)
        s < u


def test_lt__U_Q_raise_TypeError():
    with pytest.raises(TypeError):
        q = Q(1200.0)
        u = qty.Undefined(1200.0)
        u < q


def test_lt__U_S_raise_TypeError():
    with pytest.raises(TypeError):
        u = qty.Undefined(1200.0)
        s = qty.Scalar(1200.0)
        u < s


# -----------------------------------------------------------------------------
def test_update__value():
    q = Q(12.0, 'u')
    qr = q.update(value=14.0)
    qc = Q(14.0, 'u')
    assert(qc == qr)


def test_update__unit():
    q = Q(12.0, 'u')
    qr = q.update(unit='ku')
    qc = Q(12.0, 'ku')
    assert(qc == qr)


def test_update__value_and_unit():
    q = Q(12.0, 'u')
    qr = q.update(value=14.0, unit='ku')
    qc = Q(14.0, 'ku')
    assert(qc == qr)


# -----------------------------------------------------------------------------
def test_add__Qu_Qu__Qu():
    q0 = Q(6.0, 'u')
    q1 = Q(3.0, 'u')
    qr = q0 + q1
    qc = Q(9.0)
    assert(qc == qr)


def test_add__Qu_Qv__Qu():
    q0 = Q(6000.0, 'u')
    q1 = Q(3.0, 'ku')
    qr = q0 + q1
    qc = Q(9000.0, 'u')
    assert(qc == qr)

def test_add__Qu_Pu__raise_TypeError():
    q = Q(12.0, 'u')
    p = P(12.0, 'u')
    with pytest.raises(TypeError):
        q + p


def test_add__Q_S__raise_TypeError():
    q = Q(12.0, 'u')
    s = qty.Scalar(12.0)
    with pytest.raises(TypeError):
        q + s


def test_add__Q_U__raise_TypeError():
    q = Q(12.0, 'u')
    u = qty.Undefined(12.0)
    with pytest.raises(TypeError):
        q + u


def test_add__S_Q__raise_TypeError():
    s = qty.Scalar(12.0)
    q = Q(12.0, 'u')
    with pytest.raises(TypeError):
        s + q


def test_add__U_Q__raise_TypeError():
    u = qty.Undefined(12.0)
    q = Q(12.0, 'u')
    with pytest.raises(TypeError):
        u + q


def test_add__S_U__raise_TypeError():
    s = qty.Scalar(12.0)
    u = qty.Undefined(12.0)
    with pytest.raises(TypeError):
        s + u


def test_add__U_S__raise_TypeError():
    u = qty.Undefined(12.0)
    s = qty.Scalar(12.0)
    with pytest.raises(TypeError):
        u + s

def test_add__S_S__S():
    s0 = qty.Scalar(6.0)
    s1 = qty.Scalar(3.0)
    r = s0 + s1
    c = qty.Scalar(9.0)
    assert(c == r)

def test_add__U_U__U():
    u0 = qty.Undefined(6.0)
    u1 = qty.Undefined(3.0)
    r = u0 + u1
    c = qty.Undefined(9.0)
    assert(c == r)

# -----------------------------------------------------------------------------
def test_sub__Qu_Qu__Qu():
    q0 = Q(6.0, 'u')
    q1 = Q(3.0, 'u')
    qr = q0 - q1
    qc = Q(3.0)
    assert(qc == qr)


def test_sub__Qu_Qv__Qu():
    q0 = Q(6000.0, 'u')
    q1 = Q(3.0, 'ku')
    qr = q0 - q1
    qc = Q(3000.0, 'u')
    assert(qc == qr)

def test_sub__Qu_Pu__raise_TypeError():
    q = Q(12.0, 'u')
    p = P(12.0, 'u')
    with pytest.raises(TypeError):
        q - p


def test_sub__Q_S__raise_TypeError():
    q = Q(12.0, 'u')
    s = qty.Scalar(12.0)
    with pytest.raises(TypeError):
        q - s


def test_sub__Q_U__raise_TypeError():
    q = Q(12.0, 'u')
    u = qty.Undefined(12.0)
    with pytest.raises(TypeError):
        q - u


def test_sub__S_Q__raise_TypeError():
    s = qty.Scalar(12.0)
    q = Q(12.0, 'u')
    with pytest.raises(TypeError):
        s - q


def test_sub__U_Q__raise_TypeError():
    u = qty.Undefined(12.0)
    q = Q(12.0, 'u')
    with pytest.raises(TypeError):
        u - q


def test_sub__S_U__raise_TypeError():
    s = qty.Scalar(12.0)
    u = qty.Undefined(12.0)
    with pytest.raises(TypeError):
        s - u


def test_sub__U_S__raise_TypeError():
    u = qty.Undefined(12.0)
    s = qty.Scalar(12.0)
    with pytest.raises(TypeError):
        u - s

def test_sub__S_S__S():
    s0 = qty.Scalar(6.0)
    s1 = qty.Scalar(3.0)
    r = s0 - s1
    c = qty.Scalar(3.0)
    assert(c == r)

def test_sub__U_U__U():
    u0 = qty.Undefined(6.0)
    u1 = qty.Undefined(3.0)
    r = u0 - u1
    c = qty.Undefined(3.0)
    assert(c == r)

# -----------------------------------------------------------------------------
def test_mul__Qu_Qu__U():
    q0 = Q(6.0, 'u')
    q1 = Q(3.0, 'u')
    qr = q0 * q1
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__Qu_Qv__Uu():
    q0 = Q(6.0, 'ku')
    q1 = Q(3000.0, 'u')
    qr = q0 * q1
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__Q_S__Q():
    q = Q(6.0)
    s = qty.Scalar(3.0)
    qr = q * s
    qc = Q(18.0)
    assert(qc == qr)


def test_mul__Q_U__U():
    q = Q(6.0)
    u = qty.Undefined(3.0)
    qr = q * u
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__S_S__S():
    s0 = qty.Scalar(3.0)
    s1 = qty.Scalar(6.0)
    qr = s0 * s1
    qc = qty.Scalar(18.0)
    assert(qc == qr)


def test_mul__S_Q__Q():
    s = qty.Scalar(3.0)
    q = Q(6.0)
    qr = s * q
    qc = Q(18.0)
    assert(qc == qr)


def test_mul__S_U__U():
    s = qty.Scalar(6.0)
    u = qty.Undefined(3.0)
    qr = s * u
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__U_U__U():
    u0 = qty.Undefined(3.0)
    u1 = qty.Undefined(6.0)
    qr = u0 * u1
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__U_Q__U():
    u = qty.Undefined(3.0)
    q = Q(6.0)
    qr = u * q
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__U_S__U():
    u = qty.Undefined(3.0)
    s = qty.Scalar(6.0)
    qr = u * s
    qc = qty.Undefined(18.0)
    assert(qc == qr)


def test_mul__S_int__S():
    a = qty.Scalar(2.0)
    b = 3
    sr = a * b
    sc = qty.Scalar(6.0)
    assert (sc == sr)


def test_mul__S_float__S():
    a = qty.Scalar(2.0)
    b = 3.0
    sr = a * b
    sc = qty.Scalar(6.0)
    assert (sc == sr)


def test_mul__U_int__U():
    a = qty.Undefined(2.0)
    b = 3
    sr = a * b
    sc = qty.Undefined(6.0)
    assert (sc == sr)


def test_mul__U_float__U():
    a = qty.Undefined(2.0)
    b = 3.0
    sr = a * b
    sc = qty.Undefined(6.0)
    assert (sc == sr)


# -----------------------------------------------------------------------------
def test_tdiv__Qu_Qu__S():
    q0 = Q(6.0, 'u')
    q1 = Q(3.0, 'u')
    qr = q0 / q1
    qc = qty.Scalar(2.0)
    assert(qc == qr)


def test_tdiv__Qu_Qv__S():
    q0 = Q(6.0, 'ku')
    q1 = Q(3000.0, 'u')
    qr = q0 / q1
    qc = qty.Scalar(2.0)
    assert(qc == qr)


def test_tdiv__Q_S__Q():
    q = Q(6.0)
    s = qty.Scalar(3.0)
    qr = q / s
    qc = Q(2.0)
    assert(qc == qr)


def test_tdiv__Q_U__U():
    q = Q(6.0)
    u = qty.Undefined(3.0)
    qr = q / u
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__S_S__S():
    s0 = qty.Scalar(6.0)
    s1 = qty.Scalar(3.0)
    qr = s0 / s1
    qc = qty.Scalar(2.0)
    assert(qc == qr)


def test_tdiv__S_Q__U():
    s = qty.Scalar(6.0)
    q = Q(3.0)
    qr = s / q
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__S_U__U():
    s = qty.Scalar(6.0)
    u = qty.Undefined(3.0)
    qr = s / u
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__U_U__U():
    u0 = qty.Undefined(6.0)
    u1 = qty.Undefined(3.0)
    qr = u0 / u1
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__U_Q__U():
    u = qty.Undefined(6.0)
    q = Q(3.0)
    qr = u / q
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__U_S__U():
    u = qty.Undefined(6.0)
    s = qty.Scalar(3.0)
    qr = u / s
    qc = qty.Undefined(2.0)
    assert(qc == qr)


def test_tdiv__S_int__S():
    a = qty.Scalar(6.0)
    b = 3
    sr = a / b
    sc = qty.Scalar(2.0)
    assert (sc == sr)


def test_tdiv__S_float__S():
    a = qty.Scalar(6.0)
    b = 3.0
    sr = a / b
    sc = qty.Scalar(2.0)
    assert (sc == sr)


def test_tdiv__U_int__U():
    a = qty.Undefined(6.0)
    b = 3
    sr = a / b
    sc = qty.Undefined(2.0)
    assert (sc == sr)


def test_tdiv__U_float__U():
    a = qty.Undefined(6.0)
    b = 3.0
    sr = a / b
    sc = qty.Undefined(2.0)
    assert (sc == sr)


# -----------------------------------------------------------------------------
def test_fdiv__Qu_Qu__S():
    q0 = Q(10.0, 'u')
    q1 = Q(3.0, 'u')
    r = q0 // q1
    c = qty.Scalar(3.0)
    assert(r == c)


def test_fdiv__Qu_Qv__S():
    q0 = Q(10.0, 'ku')
    q1 = Q(3000.0, 'u')
    r = q0 // q1
    c = qty.Scalar(3.0)
    assert(r == c)


def test_fdiv__S_S__S():
    s0 = qty.Scalar(10.0)
    s1 = qty.Scalar(3.0)
    r = s0 // s1
    c = qty.Scalar(3.0)
    assert (c == r)


def test_fdiv__S_Q__U():
    s = qty.Scalar(10.0)
    q = Q(3.0)
    r = s // q
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__S_U__U():
    s = qty.Scalar(10.0)
    u = qty.Undefined(3.0)
    r = s // u
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__U_U__U():
    u0 = qty.Undefined(10.0)
    u1 = qty.Undefined(3.0)
    r = u0 // u1
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__U_Q__U():
    u = qty.Undefined(10.0)
    q = Q(3.0)
    r = u // q
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__U_S__U():
    u = qty.Undefined(10.0)
    s = qty.Scalar(3.0)
    r = u // s
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__S_int__S():
    s = qty.Scalar(10.0)
    i = 3
    r = s // i
    c = qty.Scalar(3.0)
    assert (c == r)


def test_fdiv__S_float__S():
    s = qty.Scalar(10.0)
    f = 3.0
    r = s // f
    c = qty.Scalar(3.0)
    assert (c == r)


def test_fdiv__U_int__U():
    u = qty.Undefined(10.0)
    i = 3
    r = u // i
    c = qty.Undefined(3.0)
    assert (c == r)


def test_fdiv__U_float__U():
    u = qty.Undefined(10.0)
    f = 3.0
    r = u // f
    c = qty.Undefined(3.0)
    assert (c == r)

