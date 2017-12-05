# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 15:17:00 2017
@author: Jérémie Fache
"""
import numpy as _np
import operator as _operator
import math as _math
from collections import namedtuple as _nt
from abc import (ABCMeta as _ABCMeta,
                 abstractmethod as _abstractmethod,
                 )


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class _ClassProperty(property):
    def __get__(self, cls, objtype):
#        print('self:{}  cls:{} objtype:{}'.format(self, cls, objtype))
        return self.fget.__get__(None, objtype)(objtype)

    def __set__(self, obj, value):
        raise AttributeError("Read only property")


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class BaseQuantity(metaclass=_ABCMeta):
    """
    Abstract base class that exposes a common interface and behaviour
    to Scalar, Undefined and Quantity.

    """
    def __init__(self, value, unit, units):
        if unit not in units:
            raise KeyError('"{}" is a wrong unit , '
                           'must be one of {}'.format(unit, units))

        self.__value = value
        self.__unit = unit
        self.__units = units

# IMPLEMENTED PROPERTIES ------------------------------------------------------
    @property
    def value(self):
        """
        Returns the current value.
        """
        return self.__value

    @property
    def unit(self):
        """
        Returns the current unit (str).
        """
        return self.__unit

    @property
    def items(self):
        """
        Property which returns a namedtuple *Items* with fields
        (*qtype, value, unit*).

        * *qtype* : quantity type (class)
        * *value* : numerical value
        * *unit* : current unit (str)
        """
        return _nt('Items', 'qtype, value, unit')(
                qtype=type(self),
                value=self.value,
                unit=self.unit)

    @property
    def auto(self):
        """
        Property which returns a new quantity converted to a unit which
        minimizes exponent.
        """
        try:
            self.value.ndim
            raise ValueError("Quantity does not support auto property for "
                             "numpy array. numpy array: {}".format(self.value))
        except AttributeError:
            pass

        def compute_abs_decade(x):
            if x == 0.0:
                return 0
            else:
                return abs(int(_math.log10(abs(x))))

        best_unit = min(self.units, key=lambda u: compute_abs_decade(self[u]))
        return self.to(best_unit)

    @_ClassProperty
    def units(objtype):
        """
        Returns a tuple of valid units for this quantity.
        """
        return objtype.__units__()

    @_ClassProperty
    def symbol(objtype):
        """
        Returns the quantity symbol.
        """
        return objtype.__symbol__()

    @_ClassProperty
    def tag(objtype):
        """
        Returns the quantity name.
        """
        return objtype.__tag__()

# ABSTRACT METHODS ------------------------------------------------------------
    @staticmethod
    @_abstractmethod
    def __units__():
        """
        See *BaseQuantity.units* property.
        """
        pass

    @staticmethod
    @_abstractmethod
    def __symbol__():
        """
        See *BaseQuantity.symbol* property.
        """
        pass

    @staticmethod
    @_abstractmethod
    def __tag__():
        """
        See *BaseQuantity.tag* property.
        """
        pass

    @_abstractmethod
    def to(self, unit):
        """
        Returns a new quantity converted to the specified unit.

        Raises
        ======
        KeyError
            Raised if *unit* argument is not a valid unit. One should check
            valid units by calling *.units* property.

        """
        pass

# METHODS ---------------------------------------------------------------------
    def update(self, value=None, unit=None):
        """
        Returns a new instance replacing value and/or unit.
        """
        if value is None:
            v = self.value
        else:
            v = value

        if unit is None:
            u = self.unit
        else:
            u = unit
        return self.__class__(v, u)

# MAGIC METHODS ---------------------------------------------------------------
    def __repr__(self):
        return '{}{}'.format(self.value, self.unit)

    def __eq__(self, other):
#        return isinstance(other, type(self)) and \
#                self.value == other.to(self.unit).value

        if not isinstance(other, type(self)):
            return False

        # same type of quantity
        # check for numpy array
        if isinstance(self.value, _np.ndarray):
            if isinstance(other.value, _np.ndarray):
                # other and self are numpy array
                other_val = other.to(self.unit).value
                return _np.all(other_val == self.value)

            else:
                # self is numpy array but not other
                return False

        else:
            if isinstance(other.value, _np.ndarray):
                # other is numpy array but not self
                return False
            else:
                # self and other are not numpy array
                return self.value == other.to(self.unit).value


    def __add__(self, other):
        if isinstance(other, type(self)):
            rvalue = self.value + other.to(self.unit).value
            return self.__class__(rvalue, self.unit)
        else:
            raise TypeError('Operands must be of the same '
                            'type: {} + {} '.format(self, other))

    def __sub__(self, other):
        if isinstance(other, type(self)):
            rvalue = self.value - other.to(self.unit).value
            return self.__class__(rvalue, self.unit)
        else:
            raise TypeError('Operands must be of the same '
                            'type: {} - {} '.format(self, other))

    def __mul__(self, other):
        raise NotImplementedError

    def __truediv__(self, other):
        raise NotImplementedError

    def __floordiv__(self, other):
        raise NotImplementedError

    def __getitem__(self, key):
        return self.to(key).value

    def __abs__(self):
        return self.__class__(abs(self.value), self.unit)

    def __gt__(self, other):
        return self._compare(other, _operator.gt)

    def __ge__(self, other):
        return self._compare(other, _operator.ge)

    def __lt__(self, other):
        return self._compare(other, _operator.lt)

    def __le__(self, other):
        return self._compare(other, _operator.le)

    def __len__(self):
        return len(self.__value)

    def _compare(self, other, op):
        if isinstance(other, type(self)):
            return op(self.value, other.to(self.unit).value)
        else:
            raise TypeError('Operands must be of the same '
                            'type: {} {} '.format(self, other))


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Quantity(BaseQuantity):
    """
    Class inherited from BaseQuantity that implements or override
    some behaviour.

    This class must be subclassed and **must not be instanciated** directly.

    Subclassing details
    ===================
    The __init__(*value, unit, units*) method must be called during
    subclass instanciation.

    Abstract methods that must be implemented:

    * to(self)
    * __units__() with @staticmethod decorator
    * __tag__()  with @staticmethod decorator
    * __symbol__() with @staticmethod decorator


    Math behaviour
    ==============
    - **q**: quantity object
    - **s**: scalar object
    - **u**: undefined object

    Multiplication
        * q x q : u
        * s x q : q
        * q x s : q
        * q x u : u
        * u x q : u

    True and floor division
        * q / q : s
        * s / q : u
        * q / s : q
        * u / q : u
        * q / u : u

    Addition and substraction
        * q +- q : q
        * s +- q : TypeError
        * q +- s : TypeError
        * u +- q : TypeError
        * q +- u : TypeError

    """

# -----------------------------------------------------------------------------
    def _div(self, other, op):
        if isinstance(other, BaseQuantity):
            # Q / Undef -> Undef
            if isinstance(other, Undefined):
                v = op(self.value, other.value)
                return Undefined(v)

            # Q / Scalar -> Q
            if isinstance(other, Scalar):
                v = op(self.value, other.value)
                return self.__class__(v, self.unit)

            # Q / Q -> Scalar   (different to mul)
            if isinstance(other, type(self)):
                v = op(self.value, other.to(self.unit).value)
                return Scalar(v)

            # Qa / Qb -> Undef
            v = op(self.value, other.value)
            return Undefined(v)

        else:
            # Q / x -> Q (assumes x is a scalar)
            v = op(self.value, other)
            return self.__class__(v, self.unit)

# -----------------------------------------------------------------------------
    def _mul(self, other):
        op = _operator.mul
        if isinstance(other, BaseQuantity):
            # Q * Undef -> Undef
            if isinstance(other, Undefined):
                v = op(self.value, other.value)
                return Undefined(v)

            # Q * Scalar -> Q
            if isinstance(other, Scalar):
                v = op(self.value, other.value)
                return self.__class__(v, self.unit)

            # Q * Q -> Undef   (different to div)
            if isinstance(other, type(self)):
                v = op(self.value, other.to(self.unit).value)
                return Undefined(v)

            # Qa * Qb -> Undef
            v = op(self.value, other.value)
            return Undefined(v)

        else:
            # Q * x -> Q (assumes x is a scalar)
            v = op(self.value, other)
            return self.__class__(v, self.unit)


# -----------------------------------------------------------------------------
    def __truediv__(self, other):
        return self._div(other, _operator.truediv)


# -----------------------------------------------------------------------------
    def __floordiv__(self, other):
        return self._div(other, _operator.floordiv)

# -----------------------------------------------------------------------------
    def __mul__(self, other):
        return self._mul(other)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Scalar(BaseQuantity):
    """
    Represents a scalar.

    Can be use to perform math operation with quantities object.

    Math behaviour
    ==============
    - **q**: quantity object
    - **s**: scalar object
    - **u**: undefined object

    Multiplication
        * s x s : s
        * s x q : q
        * q x s : q
        * s x u : u
        * u x s : u

    True and floor division
        * s / s : s
        * s / q : u
        * q / s : q
        * s / u : u
        * u / s : u

    Addition and substraction
        * s +- s : s
        * s +- q : TypeError
        * q +- s : TypeError
        * s +- u : TypeError
        * u +- s : TypeError
    """

    _UNIT = '@'

# -----------------------------------------------------------------------------
    def __init__(self, value=1.0, unit=None):
        self._value = value

# -----------------------------------------------------------------------------
    @property
    def value(self):
        return self._value

# -----------------------------------------------------------------------------
    @property
    def unit(self):
        return self._UNIT

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return (Scalar._UNIT,)

    @staticmethod
    def __symbol__():
        return 's'

    @staticmethod
    def __tag__():
        return 'scalar'

# -----------------------------------------------------------------------------
    def update(self, value):
        return Scalar(value)

# -----------------------------------------------------------------------------
    def to(self, unit):
        return self

# -----------------------------------------------------------------------------
    def __mul__(self, other):
        # S * Q -> Q
        # S * Undef -> Undef
        # S * S -> S
        if isinstance(other, BaseQuantity):
            rvalue = self.value * other.value
            runit = other.unit
            return other.__class__(rvalue, runit)

        # S * x -> S (assumes x is a scalar)
        else:
            rvalue = self.value * other
            return Scalar(rvalue)

# -----------------------------------------------------------------------------
    def __floordiv__(self, other):
        return self._div(other, _operator.floordiv)

# -----------------------------------------------------------------------------
    def __truediv__(self, other):
        return self._div(other, _operator.truediv)

# -----------------------------------------------------------------------------
    def _div(self, other, op):

        if isinstance(other, BaseQuantity):

            # S / Q -> U
            # S / Undef -> Undef
            # S / S -> S
            if isinstance(other, Quantity):
                rvalue = op(self.value, other.value)
                return Undefined(rvalue)

            rvalue = op(self.value, other.value)
            runit = other.unit
            return other.__class__(rvalue, runit)

        else:
            rvalue = op(self.value, other)
            return Scalar(rvalue)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Undefined(BaseQuantity):
    """
    Represents an Undefined quantity.

    Results from operations where the output quantity type differs from input
    quantity(ies) type such as 1/frequency -> time, Length^3 -> volume, etc.

    Math behaviour
    ==============
    - **q**: quantity object
    - **s**: scalar object
    - **u**: undefined object

    Multiplication
        * u x u : u
        * u x q : u
        * q x u : u
        * s x u : u
        * u x s : u

    True and floor division
        * u / u : u
        * u / q : u
        * q / u : u
        * s / u : u
        * u / s : u

    Addition and substraction
        * u +- u : u
        * u +- q : TypeError
        * q +- s : TypeError
        * s +- u : TypeError
        * u +- s : TypeError
    """

    _UNIT = '?'

# -----------------------------------------------------------------------------
    def __init__(self, value=1.0, unit=None):
        if isinstance(value, BaseQuantity):
            if isinstance(value, Undefined):
                self._value = value.value
        else:
            self._value = value

# -----------------------------------------------------------------------------
    @property
    def value(self):
        return self._value

    @property
    def unit(self):
        return self._UNIT

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return (Undefined._UNIT,)

    @staticmethod
    def __symbol__():
        return 'u'

    @staticmethod
    def __tag__():
        return 'undefined'

# -----------------------------------------------------------------------------
    def update(self, value):
        return Undefined(value)

# -----------------------------------------------------------------------------
    def to(self, unit):
        return self

# -----------------------------------------------------------------------------
    def __mul__(self, other):
        if isinstance(other, BaseQuantity):
            return Undefined(self._value * other.value)
        else:
            return Undefined(self._value * other)

# -----------------------------------------------------------------------------
    def __floordiv__(self, other):
        if isinstance(other, BaseQuantity):
            return Undefined(self._value // other.value)
        else:
            return Undefined(self._value // other)

# -----------------------------------------------------------------------------
    def __truediv__(self, other):
        if isinstance(other, BaseQuantity):
            return Undefined(self._value / other.value)
        else:
            return Undefined(self._value / other)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Frequency(Quantity):
    """
    Represents a frequency.

    Units
    =====
    Hz, kHz, MHz, GHz

    Default: **Hz**

    """

    _UNITS = ('Hz', 'kHz', 'MHz', 'GHz')
    _FACTORS = {'Hz': 1.0, 'kHz': 1.0e3, 'MHz': 1.0e6, 'GHz': 1.0e9}

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Frequency._UNITS

    @staticmethod
    def __symbol__():
        return 'F'

    @staticmethod
    def __tag__():
        return 'frequency'

# -----------------------------------------------------------------------------
    def __init__(self, value=1.0, unit='Hz'):
        Quantity.__init__(self, value, unit, self._UNITS)


# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        try:
            f = self._FACTORS[self.unit] / self._FACTORS[unit]
        except KeyError:
            raise KeyError('<frequency> "{}" wrong unit , '
                           'must be one of {}'.format(unit, self.units))
        return Frequency(self.value * f, unit)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Length(Quantity):
    """
    Represents a length.

    Units
    =====
    m, mm, µm, nm, pm

    Default: **m**
    """

    _UNITS = ('m', 'mm', 'µm', 'nm', 'pm')
    _FACTORS = {'m': 1.0, 'mm': 1.0e-3, 'µm': 1.0e-6,
                'nm': 1.0e-9, 'pm': 1.0e-12}

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Length._UNITS

    @staticmethod
    def __symbol__():
        return 'L'

    @staticmethod
    def __tag__():
        return 'length'


# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='m'):
        Quantity.__init__(self, value, unit, self._UNITS)

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        try:
            f = self._FACTORS[self.unit] / self._FACTORS[unit]
        except KeyError:
            raise KeyError('<length> "{}" wrong unit , '
                           'must be one of {}'.format(unit, self._UNITS))
        return Length(self.value * f, unit)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Time(Quantity):
    """
    Represents a time.

    Units
    =====
    s, ms, µs, ns

    Default: **s**
    """

    _UNITS = ('s', 'ms', 'µs', 'ns')
    _FACTORS = {'s': 1.0,
                'ms': 1.0e-3,
                'µs': 1.0e-6,
                'ns': 1.0e-9}

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Time._UNITS

    @staticmethod
    def __symbol__():
        return 't'

    @staticmethod
    def __tag__():
        return 'time'


# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='s'):
        Quantity.__init__(self, value, unit, self._UNITS)

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        try:
            f = self._FACTORS[self.unit] / self._FACTORS[unit]
        except KeyError:
            raise KeyError('<Time> "{}" wrong unit , '
                           'must be one of {}'.format(unit, self._UNITS))
        return Time(self.value * f, unit)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Speed(Quantity):
    """
    Represents a speed.

    Units
    =====
    m/s, km/h

    Default: **m/s**
    """

    _UNITS = ('m/s', 'mm/s', 'km/h')
    _FACTORS = {'m/s': 1.0, 'mm/s': 1000.0, 'km/h': 3.6}

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Speed._UNITS

    @staticmethod
    def __symbol__():
        return 'S'

    @staticmethod
    def __tag__():
        return 'speed'


# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='m/s'):
        Quantity.__init__(self, value, unit, self._UNITS)

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        try:
            f = self._FACTORS[self.unit] / self._FACTORS[unit]
        except KeyError:
            raise KeyError('<speed> "{}" wrong unit , '
                           'must be one of {}'.format(unit, self._UNITS))
        return self.__class__(self.value * f, unit)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Angle(Quantity):
    """
    Represents a geometry angle.

    Units
    =====
    °, rad

    Default: **°**
    """

    _UNITS = ('°', 'rad')

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Angle._UNITS

    @staticmethod
    def __symbol__():
        return '\u0398'  # Theta

    @staticmethod
    def __tag__():
        return 'angle'

# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='°'):
        Quantity.__init__(self, value, unit, self._UNITS)


# -----------------------------------------------------------------------------
    def _deg_to_rad(self):
        return Angle(_np.radians(self.value), '°')
#        return Angle(_math.radians(self.value), 'rad')

# -----------------------------------------------------------------------------
    def _rad_to_deg(self):
        return Angle(_np.degrees(self.value), '°')
#        return Angle(_math.degrees(self.value), '°')

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        if unit not in self._UNITS:
            raise KeyError('<angle> "{}" wrong unit , '
                           'must be one of {}'.format(unit, self._UNITS))

        if unit == '°':
            return self._rad_to_deg()
        else:
            return self._deg_to_rad()


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class Temperature(Quantity):
    """
    Represents an absolute temperature.

    Units
    =====
    °C, °K

    Default: **°C**
    """

    _UNITS = ('°C', '°K')

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return Temperature._UNITS

    @staticmethod
    def __symbol__():
        return 'T'

    @staticmethod
    def __tag__():
        return 'temperature'

# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='°C'):
        Quantity.__init__(self, value, unit, self._UNITS)

#        if unit == '°C' and value < -273.15:
#            raise ValueError('<temperature> must be greater than -273.15°C.'
#                             ' Got {}'.format(value))
#
#        if unit == '°K' and value < 0.0:
#            raise ValueError('<temperature> must be greater than 0.0°K.'
#                             ' Got {}'.format(value))

# -----------------------------------------------------------------------------
    def _Kelvin_to_Celcius(self, T):
        return T - 273.15

    def _Celcius_to_Kelvin(self, T):
        return T + 273.15

# -----------------------------------------------------------------------------
    def __add__(self, other):
        if isinstance(other, Temperature):
            value = self.value + other[self.unit]
            return DTemperature(value=value, unit=self.unit)

        if isinstance(other, DTemperature):
            value = self.value + other[self.unit]
            return self.update(value=value)

        return super().__add__(other)

# -----------------------------------------------------------------------------
    def __sub__(self, other):
        if isinstance(other, Temperature):
            value = self.value - other[self.unit]
            return DTemperature(value=value, unit=self.unit)

        if isinstance(other, DTemperature):
            value = self.value - other[self.unit]
            return self.update(value=value)

        return super().__sub__(other)

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        if unit == '°C':
            value = self._Celcius_to_Kelvin(self.value)
            return Temperature(value, '°K')

        if unit == '°K':
            value = self._Kelvin_to_Celcius(self.value)
            return Temperature(value, '°C')

        raise KeyError('<temperature> "{}" wrong unit , '
                       'must be one of {}'.format(unit, self._UNITS))


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class DTemperature(Quantity):
    """
    Represents a temperature difference.

    Units
    =====
    °C, °K

    Default: **°C**
    """

    _UNITS = ('°C', '°K')

# -----------------------------------------------------------------------------
    @staticmethod
    def __units__():
        return DTemperature._UNITS

    @staticmethod
    def __symbol__():
        return 'ΔT'

    @staticmethod
    def __tag__():
        return 'Δtemperature'

# -----------------------------------------------------------------------------
    def __init__(self, value=0.0, unit='°C'):
        Quantity.__init__(self, value, unit, self._UNITS)

# -----------------------------------------------------------------------------
    def to(self, unit):
        if unit == self.unit:
            return self

        if unit == '°C':
            return DTemperature(self.value, '°K')

        if unit == '°K':
            return DTemperature(self.value, '°C')

        raise KeyError('<Δtemperature> "{}" wrong unit , '
                       'must be one of {}'.format(unit, self._UNITS))


# -----------------------------------------------------------------------------
    def __repr__(self):
        s = super().__repr__()
        return s + ' ΔT'
# -----------------------------------------------------------------------------
    def __add__(self, other):
        if isinstance(other, Temperature):
            value = self.value + other[self.unit]
            return Temperature(value=value, unit=self.unit)

        return super().__add__(other)

# -----------------------------------------------------------------------------
    def __sub__(self, other):
        if isinstance(other, Temperature):
            value = self.value - other[self.unit]
            return Temperature(value=value, unit=self.unit)

        return super().__add__(other)
