# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 09:39:25 2017

@author: Jérémie Fache
"""
import pytest
from .test_custom_quantities import (P, Q)
from moebius.constraint import (QConstraint, qpoint, qinterval, NoConstraint)


def test_NoConstraint_verify():
    c = NoConstraint(str)
    assert(c.verify('toto'))


def test_NoConstraint_verify_with_wrong_type_raises_TypeError():
    c = NoConstraint(str)
    with pytest.raises(TypeError):
        c.verify(12)


def test_QConstraint_verify_no_constraint():
    c = QConstraint(Q)
    assert(c.verify(Q(12.0)))
    assert(c.verify(Q(-12.0)))


def test_QConstraint_verify_with_wrong_type_raise_TypeError():
    c = QConstraint(Q)
    with pytest.raises(TypeError):
        c.verify(P(12.0))


def test_exclude_qpoint():
    c = QConstraint(Q) - qpoint(12.0)
    assert(c.verify(Q(11.0)))
    assert(c.verify(Q(11.9)))
    assert(not c.verify(Q(12.0)))
    assert(c.verify(Q(12.1)))
    assert(c.verify(Q(-12.0)))


def test_exclude_qpoint_with_delta():
    c = QConstraint(Q) - qpoint(12.0, delta=1.0)
    assert(c.verify(Q(10.0)))
    assert(c.verify(Q(10.9)))
    assert(not c.verify(Q(11.0)))
    assert(not c.verify(Q(13.0)))
    assert(c.verify(Q(13.1)))
    assert(c.verify(Q(-12.0)))


def test_exclude_qpoint_custom_unit():
    c = QConstraint(Q) - qpoint(12.0, 'ku')
    assert(c.verify(Q(11000.0)))
    assert(c.verify(Q(11900.0)))
    assert(not c.verify(Q(12000.0)))
    assert(c.verify(Q(12100.0)))
    assert(c.verify(Q(-12000.0)))


def test_include_qinterval():
    c = QConstraint(Q) + qinterval(-1.0, 5.0)
    assert(not c.verify(Q(-10.0)))
    assert(not c.verify(Q(-1.1)))
    assert(c.verify(Q(-1.0)))
    assert(c.verify(Q(2.0)))
    assert(c.verify(Q(5.0)))
    assert(not c.verify(Q(5.1)))
    assert(not c.verify(Q(12.0)))


def test_include_qinterval_open_open():
    c = QConstraint(Q) + qinterval(-1.0, 5.0, closure='][')
    assert(not c.verify(Q(-10.0)))
    assert(not c.verify(Q(-1.1)))
    assert(not c.verify(Q(-1.0)))
    assert(c.verify(Q(-0.9)))
    assert(c.verify(Q(2.0)))
    assert(c.verify(Q(4.9)))
    assert(not c.verify(Q(5.0)))
    assert(not c.verify(Q(5.1)))
    assert(not c.verify(Q(12.0)))


def test_include_qinterval_open_close():
    c = QConstraint(Q) + qinterval(-1.0, 5.0, closure=']]')
    assert(not c.verify(Q(-10.0)))
    assert(not c.verify(Q(-1.1)))
    assert(not c.verify(Q(-1.0)))
    assert(c.verify(Q(-0.9)))
    assert(c.verify(Q(2.0)))
    assert(c.verify(Q(4.9)))
    assert(c.verify(Q(5.0)))
    assert(not c.verify(Q(5.1)))
    assert(not c.verify(Q(12.0)))


def test_include_qinterval_close_open():
    c = QConstraint(Q) + qinterval(-1.0, 5.0, closure='[[')
    assert(not c.verify(Q(-10.0)))
    assert(not c.verify(Q(-1.1)))
    assert(c.verify(Q(-1.0)))
    assert(c.verify(Q(-0.9)))
    assert(c.verify(Q(2.0)))
    assert(c.verify(Q(4.9)))
    assert(not c.verify(Q(5.0)))
    assert(not c.verify(Q(5.1)))
    assert(not c.verify(Q(12.0)))


def test_include_qinterval__value_inf__close_open():
    c = QConstraint(Q) + qinterval(12.0, None)
    assert(not c.verify(Q(-12.0)))
    assert(not c.verify(Q(11.9)))
    assert(c.verify(Q(12.0)))
    assert(c.verify(Q(1000.0)))


def test_include_qinterval__inf_value__open_close():
    c = QConstraint(Q) + qinterval(None, 12.0)
    assert(c.verify(Q(-1000.0)))
    assert(c.verify(Q(-12.0)))
    assert(c.verify(Q(12.0)))
    assert(not c.verify(Q(12.1)))
    assert(not c.verify(Q(1000.0)))



