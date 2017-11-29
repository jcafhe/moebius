# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 13:21:52 2017

@author: Jérémie Fache
"""

import operator as _operator
from functools import reduce as _reduce
from collections import namedtuple as _nt
from abc import (ABCMeta as _ABCMeta,
                 abstractmethod as _abstractmethod)

import moebius.quantity as qty


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class BaseConstraint(metaclass=_ABCMeta):
    """
    Base interface for constraint classes.

    Classes inherited from BaseConstraint should hold a set of constraints
    to be verified.

    """

    @_abstractmethod
    def verify(self, obj):
        """
        Tests *obj* against all constraints and returns True if *obj*
        conforms to constraints, False if not.

        Raises:
        ========
        TypeError:
            Raised if *obj* argument is not of the expected type.
        """
        pass

    @property
    @_abstractmethod
    def objtype(self):
        """
        Returns the expected type of object to be verify.
        """
        pass


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class NoConstraint(BaseConstraint):
    def __init__(self, objtype):
        self._objtype = objtype

# -----------------------------------------------------------------------------
    def verify(self, obj):
        if type(obj) is not self._objtype:
            raise TypeError('Cannot verify a instance of type {} with a '
                            'constraint for type {}'.format(type(obj),
                                                            self._objtype))
        return True

# -----------------------------------------------------------------------------
    @property
    def objtype(self):
        return self._objtype


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
QTest = _nt('QTest', 'optype, set')
Q_OPTYPES = _nt('Q_OPTYPES', 'include, exclude')(
                            include='include',
                            exclude='exclude')


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class QConstraint(BaseConstraint):
    """
    Represents one or more constraints on a BaseQuantity.

    Holds a group of constraints on a BaseQuantity. One can chain
    constraints by using classes inherited from QBaseSet (QInterval, QPoint, etc.)
    and add/sub operators (+, -). The add operator will *include* the right
    handed set, whereas the sub operator will *exclude* the set. One can
    also call *include(item)* and *exclude(item)* methods at the cost of
    increasing verbosity.

    QConstraint is immutable which means that every calls to *include()* or
    *exclude()* methods as well as + or - operators will return a new
    instance of QConstraint.

    Examples
    ========
    Example below shows how to create a QConstraint instance which could verify
    if a Length object is in range [0m, 20m].

    >>> low = Length(0, 'm')
    >>> high = Length(20, 'm')
    >>> c = QConstraint(Length) + QInterval(low, high)
    >>> c
    <length>  include:[0m, 20m]
    >>> c.verify(Length(-2))
    False
    >>> c.verify(Length(10))
    True

    Helper functions avoids to create possibly multiple Quantity objects to
    create Set Objects. These are automaticaly created and stored in
    QConstraint.

    >>> c = QConstraint(Length) + qinterval(0, 20, 'm')
    >>> c
    <length>  include:[0m, 20m]


    One can chain multiple sets. Example below shows how to create a QConstraint
    instance for Frequency objects which could verify if a Frequency is in
    range ]0Hz, +∞[ excluding 10Kz +/-0.5.

    >>> c = QConstraint(Frequency) + qinterval(0, None, closure='][') - qpoint(10, 'kHz', delta=0.5)
    >>> c
    <frequency>  include:]0Hz, +∞[   exclude:{10kHz} +/-0.5kHz
    >>> c.verify(Frequency(0.0, 'Hz'))
    False
    >>> c.verify(Frequency(10.0, 'Hz'))
    True
    >>> c.verify(Frequency(10500.0, 'Hz'))
    False
    >>> c.verify(Frequency(10.6, 'kHz'))
    True

    """

    def __init__(self, qtype, tests=None):
        self._tests = ()
        self._qtype = qtype

        if not issubclass(qtype, qty.BaseQuantity):
            raise TypeError('QConstraint must be initialized with '
                            'a valid qtype. Got {}'.format(type(qtype)))

        if tests is not None:
            self._tests = tests

            for test in tests:
                if test.set.qtype is not None and self._qtype != test.set.qtype:
                    raise TypeError('Quantity type of Chained constraints '
                                    'must be of the same type. '
                                    '{} != {}'.format(self._qtype, test.set.qtype))


# -----------------------------------------------------------------------------
    @property
    def tests(self):
        """
        returns a tuple of all tests.
        """
        return self._tests

# -----------------------------------------------------------------------------
    @property
    def qtype(self):
        """
        returns the Quantity type of all tests to be verified. It is guaranted
        that all tests are of the same qtype.
        """
        return self._qtype

    @property
    def objtype(self):
        """
        returns the Quantity type of all tests to be verified. It is guaranted
        that all tests are of the same qtype.
        """
        return self._qtype


# -----------------------------------------------------------------------------
    def include(self, item):
        """
        Returns a new QConstraint instance with including a
        BaseQSet or a Quantity.
        """

        if isinstance(item, qty.BaseQuantity):
            item = QPoint(item)

        if item.qtype is None:
            return self

        tests = self._tests + (QTest('include', item), )
        return QConstraint(qtype=self._qtype, tests=tests)

# -----------------------------------------------------------------------------
    def exclude(self, item):
        """
        Returns a new QConstraint instance with excluding a
        BaseQSet or a Quantity.
        """

        if isinstance(item, qty.BaseQuantity):
            item = QPoint(item)

        if item.qtype is None:
            return self

        tests = self._tests + (QTest('exclude', item), )
        return QConstraint(qtype=self._qtype, tests=tests)

# -----------------------------------------------------------------------------
    def verify(self, quantity):
        """
        Tests *quantity* arg against all constraints and returns a boolean.

        Raises:
        ========
        TypeError:
            Raised if *quantity* argument is not of the expected type.

        details:
        ========
        For all stored tests, this object will call *include()* or
        *exclude()* methods of QBaseSet interface. One could do the same
        by retreving a tuple of tests with the *.tests* property.
        """
        if type(quantity) is not self._qtype:
            raise TypeError('Cannot verify a instance of type {} with a '
                            'constraint for type {}'.format(type(quantity),
                                                            self._qtype))

        for test in self._tests:
            if not getattr(test.set, test.optype)(quantity):
                return False

        return True

# -----------------------------------------------------------------------------
    def __add__(self, other):
        if isinstance(other, _QSetFactory):
            s = other.make(self._qtype)
            other = s

        return self.include(other)

# -----------------------------------------------------------------------------
    def __sub__(self, other):
        if isinstance(other, _QSetFactory):
            s = other.make(self._qtype)
            other = s

        return self.exclude(other)

# -----------------------------------------------------------------------------
    def __repr__(self):
        tag = '<{}>  '.format(self.qtype.tag)

        if len(self._tests) == 0:
#            return tag
            return '{} ]-∞, +∞['.format(tag)

        s = _reduce(lambda acc, t: '{}{}:{}   '.format(acc, t.optype, t.set), self.tests, tag)
        return s


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class BaseQSet(metaclass=_ABCMeta):
    """
    Set interface used to manipulate Quantities.
    """

    @_abstractmethod
    def include(self, q):
        pass

    @_abstractmethod
    def exclude(self, q):
        pass

    @property
    @_abstractmethod
    def qtype(self):
        pass


Closure = _nt('Closure', 'low, high')
CLOSE = 'CLOSE'
OPEN = 'OPEN'


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class QInterval(BaseQSet):
    """
    Represents a BaseQuantity interval.

    Examples
    ========
    Example below show how to create a Length interval from 3.0mm to 1m with
    including bounds :

    **[3.0mm, 1.0m]**

    >>> low = Length(3.0, 'mm')
    >>> high = Length(1.0, 'm')
    >>> QInterval(low, high)
    [3.0mm, 1.0m]

    Left and right closures can be specified: "[]", "]]", "][", "[[".
    Example below show how to create the same
    interval as before with excluding lower bound:

    **]3.0mm, 1.0m]**

    >>> QInterval(low, high, closure=']]')
    ]3.0mm, 1.0m]

    Infinite interval can be created by using None:

    **[3.0mm, +∞[**

    >>> QInterval(low, None)
    [3.0mm, +∞[


    """


    _CLOSURE_LOOKUP = {'[]': Closure(CLOSE, CLOSE),
                       '[[': Closure(CLOSE, OPEN),
                       ']]': Closure(OPEN, CLOSE),
                       '][': Closure(OPEN, OPEN)}

    _COMPARE_LOOKUP = {'[]': Closure(_operator.ge, _operator.le),
                       '[[': Closure(_operator.ge, _operator.lt),
                       ']]': Closure(_operator.gt, _operator.le),
                       '][': Closure(_operator.gt, _operator.lt)}

# -----------------------------------------------------------------------------
    def __init__(self, low=None, high=None, closure='[]'):
        try:
            self._t_closure = self._CLOSURE_LOOKUP[closure]
        except KeyError:
            raise ValueError('closure argument must be one '
                             'of {}'.format(tuple(self._CLOSURE_LOOKUP.keys())))

        cl = ']['
        self._type = None
        if low is not None:
            self._type = type(low)
            cl = closure[0] + cl[1]

        if high is not None:
            self._type = type(high)
            cl = cl[0] + closure[1]

        self._closure = cl

        if low is not None and high is not None:
            if not isinstance(low, type(high)):
                raise TypeError('low:{} and high:{} '
                                'must be of the same type'.format(low, high))
            if low > high:
                high, low = low, high

        self._bounds = _nt('Bounds', 'low, high')(
                          low=low,
                          high=high)

# -----------------------------------------------------------------------------
    def include(self, quantity):
        low, high = self._bounds
        closure = self._closure

        if self._type is None:
            return True

        if not isinstance(quantity, self._type):
            raise TypeError('Quantity:{} and range:{} '
                            'must be of the same type'.format(quantity, self))

        operators = self._COMPARE_LOOKUP[closure]

        if low is not None:
            if not operators.low(quantity, low):
                return False

        if high is not None:
            if not operators.high(quantity, high):
                return False

        return True

# -----------------------------------------------------------------------------
    def exclude(self, quantity):
        return not self.include(quantity)

# -----------------------------------------------------------------------------
    @property
    def qtype(self):
        return self._type

# -----------------------------------------------------------------------------
    def __repr__(self):
        bounds = self._bounds
        low = '-∞' if bounds.low is None else bounds.low
        high = '+∞' if bounds.high is None else bounds.high

        return '{}{}, {}{}'.format(self._closure[0],
                                   low,
                                   high,
                                   self._closure[1])


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class QPoint(BaseQSet):
    def __init__(self, quantity, delta=None):

        self._type = type(quantity)
        if delta is not None:
            delta = abs(delta)
        self._delta = delta
        self._quantity = quantity

        if quantity is None:
            raise ValueError('Quantity cannot be None. '
                             'None represents ]-∞, +∞[')

        if not isinstance(quantity, qty.BaseQuantity):
            raise TypeError('quantity must be one of the types Quantity, '
                            'Scalar, or Undefined. got {}'.format(quantity))

        if delta is not None and not isinstance(delta, type(quantity)):
            raise TypeError('quantity:{} and delta:{} must be of the '
                            'same type.'.format(quantity, delta))


# -----------------------------------------------------------------------------
    def include(self, quantity):
        if isinstance(quantity, type(self._quantity)):
            if self._delta is None:
                return self._quantity == quantity
            else:
                return abs(self._quantity - quantity) <= self._delta

        else:
            raise TypeError('Quantities:{} and {} '
                            'must be of the same type'.format(quantity, self))

# -----------------------------------------------------------------------------
    def exclude(self, quantity):
        return not self.include(quantity)

# -----------------------------------------------------------------------------
    @property
    def delta(self):
        return self._delta

# -----------------------------------------------------------------------------
    @property
    def quantity(self):
        return self._quantity

# -----------------------------------------------------------------------------
    @property
    def qtype(self):
        return self._type

# -----------------------------------------------------------------------------
    def __repr__(self):
        if self._delta is None:
            return '{{{}}}'.format(self._quantity)
        else:
            return '{{{}}} +/-{}'.format(self._quantity, self._delta)

class _QSetFactory(object):
    def make(self, qtype):
        raise NotImplementedError


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def qinterval(low=None, high=None, unit=None, closure='[]'):

    class RangeFactory(_QSetFactory):
        def make(self, qtype):
            ql = low
            if low is not None:
                if unit is None:
                    ql = qtype(low)
                else:
                    ql = qtype(low, unit)

            qh = high
            if high is not None:
                if unit is None:
                    qh = qtype(high)
                else:
                    qh = qtype(high, unit)

            return QInterval(low=ql, high=qh, closure=closure)

    return RangeFactory()


# -----------------------------------------------------------------------------
def qpoint(value, unit=None, delta=None):
    class PointFactory(_QSetFactory):
        def make(self, qtype):
            d = delta

            if value is None:
                raise ValueError('qpoint cannot be None')

            if unit is not None:
                q = qtype(value, unit)
                if d is not None:
                    d = qtype(delta, unit)
            else:
                q = qtype(value)
                if d is not None:
                    d = qtype(delta)

            return QPoint(q, d)

    return PointFactory()