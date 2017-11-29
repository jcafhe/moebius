# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 12:20:48 2017

@author: Jérémie Fache
"""
import pytest
import moebius.quantity as qty
from .test_custom_quantities import (P, Q)
from moebius.constraint import (QInterval, QPoint)


def test_QPoint_include():
    p = QPoint(Q(1.0))
    assert(not p.include(Q(+0.9, 'u')))
    assert(p.include(Q(+1.0, 'u')))
    assert(not p.include(Q(+1.1, 'u')))
    assert(not p.include(Q(-1.0, 'u')))

def test_QPoint_include_different_unit():
    p = QPoint(Q(1.0, 'ku'))
    assert(not p.include(Q(+900.0, 'u')))
    assert(p.include(Q(+1000.0, 'u')))
    assert(not p.include(Q(+1100.0, 'u')))
    assert(not p.include(Q(-1000.0, 'u')))

def test_QPoint_include_with_delta():
    #range [-1.0, 3.0]
    p = QPoint(Q(1.0), Q(2.0))
    assert(not p.include(Q(-1.1, 'u')))
    assert(p.include(Q(-1.0, 'u')))
    assert(p.include(Q(+1.0, 'u')))
    assert(p.include(Q(+3.0, 'u')))
    assert(not p.include(Q(+3.1, 'u')))

def test_QPoint_include_with_delta_different_unit():
    #range [-1.0, 3.0]
    p = QPoint(Q(1.0e-3, 'ku'), Q(2.0e-3, 'ku'))
    assert(not p.include(Q(-1.1, 'u')))
    assert(p.include(Q(-1.0, 'u')))
    assert(p.include(Q(+1.0, 'u')))
    assert(p.include(Q(+3.0, 'u')))
    assert(not p.include(Q(+3.1, 'u')))

def test_QPoint_exclude():
    p = QPoint(Q(1.0))
    assert(p.exclude(Q(+0.9, 'u')))
    assert(not p.exclude(Q(+1.0, 'u')))
    assert(p.exclude(Q(+1.1, 'u')))
    assert(p.exclude(Q(-1.0, 'u')))

def test_QPoint_exclude_with_delta():
    p = QPoint(Q(1.0), Q(2.0))
    assert(p.exclude(Q(-1.1, 'u')))
    assert(not p.exclude(Q(-1.0, 'u')))
    assert(not p.exclude(Q(+1.0, 'u')))
    assert(not p.exclude(Q(+3.0, 'u')))
    assert(p.exclude(Q(+3.1, 'u')))


# -----------------------------------------------------------------------------
def test_QInterval_include__Q_Q__close_close():
    q0 = Q(-1.0, 'u')
    q1 = Q(2.0, 'u')
    r = QInterval(q0, q1, '[]')
    assert(r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(r.include(Q(+2.0, 'u')))
    assert(not r.include(Q(-1.1, 'u')))
    assert(not r.include(Q(+2.1, 'u')))


def test_QInterval_include__Qu_Qv__close_close():
    q0 = Q(-1.0, 'u')
    q1 = Q(2.0, 'ku')
    r = QInterval(q0, q1, '[]')
    assert(r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.9, 'ku')))
    assert(r.include(Q(+1999.0, 'u')))
    assert(not r.include(Q(-1.1, 'u')))
    assert(not r.include(Q(+2.1, 'ku')))
    assert(not r.include(Q(+2100.0, 'u')))


def test_QInterval_include__Q_Q__open_close():
    q0 = Q(-1.0, 'u')
    q1 = Q(2.0, 'u')
    r = QInterval(q0, q1, ']]')
    assert(not r.include(Q(-1.1, 'u')))
    assert(not r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(r.include(Q(+2.0, 'u')))
    assert(not r.include(Q(+2.1, 'u')))


def test_QInterval_include__Q_Q__close_open():
    q0 = Q(-1.0, 'u')
    q1 = Q(2.0, 'u')
    r = QInterval(q0, q1, '[[')
    assert(not r.include(Q(-1.1, 'u')))
    assert(r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(not r.include(Q(+2.0, 'u')))
    assert(not r.include(Q(+2.1, 'u')))


def test_QInterval_include__Q_Q__open_open():
    q0 = Q(-1.0, 'u')
    q1 = Q(2.0, 'u')
    r = QInterval(q0, q1, '][')
    assert(not r.include(Q(-1.1, 'u')))
    assert(not r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(not r.include(Q(+2.0, 'u')))
    assert(not r.include(Q(+2.1, 'u')))


def test_QInterval_include__None_Q__close_close():
    q1 = Q(2.0, 'u')
    r = QInterval(None, q1, '[]')
    assert(r.include(Q(-1.1, 'u')))
    assert(r.include(Q(-1.0, 'ku')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(r.include(Q(+2.0, 'u')))
    assert(not r.include(Q(+2.1, 'u')))


def test_QInterval_include__Q_None__close_close():
    q0 = Q(-1.0, 'u')
    r = QInterval(q0, None, '[]')
    assert(not r.include(Q(-1.1, 'u')))
    assert(r.include(Q(-1.0, 'u')))
    assert(r.include(Q(+0.0, 'u')))
    assert(r.include(Q(+1.0, 'u')))
    assert(r.include(Q(+2.0, 'u')))
    assert(r.include(Q(+2.1, 'u')))


def test_QInterval_include__None_None_close_close():
    rge = QInterval(None, None)
    assert(rge.include(Q(1.0)))
    assert(rge.include(Q(-1.0)))
    assert(rge.include(Q(2.5e12)))
    assert(rge.include(Q(-2.5e12, 'ku')))


# -----------------------------------------------------------------------------
def test_QInterval_swap_when_low_is_gt_high():
    rge = QInterval(Q(+2.0), Q(-2.0))
    assert(rge.include(Q(-2.0)))
    assert(rge.include(Q(+2.0)))
    assert(rge.include(Q(0.0)))
    assert(not rge.include(Q(-2.1)))
    assert(not rge.include(Q(+2.1)))


# -----------------------------------------------------------------------------
def test_QInterval_include__Q_Q_with_P_raises_TypeError():
    with pytest.raises(TypeError):
        rge = QInterval(Q(-2.0), Q(+2.0))
        p = P(2.0)
        rge.include(p)


def test_QInterval_include__Q_None_with_P_raises_TypeError():
    with pytest.raises(TypeError):
        rge = QInterval(Q(-2.0), None)
        p = P(2.0)
        rge.include(p)


def test_QInterval_include__None_Q_with_P_raises_TypeError():
    with pytest.raises(TypeError):
        rge = QInterval(None, Q(+2.0))
        p = P(2.0)
        rge.include(p)

# -----------------------------------------------------------------------------
def test_QInterval_init__Q_P_raises_TypeError():
    with pytest.raises(TypeError):
        rge = QInterval(Q(-2.0), P(+2.0))
