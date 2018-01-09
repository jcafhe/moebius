# -*- coding: utf-8 -*-
"""
Created on Mon Aug 28 09:17:20 2017

@author: Jérémie Fache
"""
from abc import ABCMeta, abstractmethod
from collections import Iterable
import sys as _sys


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class _ClassProperty(property):
    """
    Property that can be accessed from instance or class.
    """

    def __get__(self, cls, objtype):
        return self.fget.__get__(None, objtype)(objtype)

    def __set__(self, obj, value):
        raise AttributeError("Read only property")


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
class BaseOption(metaclass=ABCMeta):
    """
    Base Interface for Option type.

    Subclass must guaranty that current value is one of the BaseOption.options
    and raises ValueError if not.
    """

    @_ClassProperty
    def options(objtype):
        """
        Returns a tuple enumerating valid values.
        """
        return objtype.__options__()

    @property
    @abstractmethod
    def value(self):
        """
        Returns current value.
        """
        pass

    @abstractmethod
    def update(self):
        pass

    @staticmethod
    @abstractmethod
    def __options__():
        """
        See BaseOption.options property.
        """
        pass

    def __repr__(self):
        return '{} in {}'.format(self.value, self.options)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
_class_template = """\
from {modulename} import BaseOption

class {typename}(BaseOption):
    _OPTIONS = {options}

    def __init__(self, value):
        self._value = value
        if value not in self.options:
            raise KeyError('Option value must be one of {{}}. '
                           'Got {{}}'.format(self._OPTIONS, value))

    @property
    def value(self):
        return self._value

    def update(self, value):
        return self.__class__(value)

    @staticmethod
    def __options__():
        return ({typename}._OPTIONS)

"""


def create_option(typename, options):
    """
    Returns a new subclass of tuple with named fields.
    """
    typename = str(typename)

    if isinstance(options, str) or not isinstance(options, Iterable):
        options = (options,)
    else:
        options = tuple(options)

    # Inspired by collections.namedtuple
    class_definition = _class_template.format(
            typename=typename,
            options=options,
            modulename=__name__)

    # Execute the template string in a temporary namespace and support
    # tracing utilities by setting a value for frame.f_globals['__name__']
    namespace = dict(__name__='option_%s' % typename)
    exec(class_definition, namespace)

    result = namespace[typename]
    result.__module__ = _sys._getframe(1).f_globals.get('__name__', '__main__')
    return result


