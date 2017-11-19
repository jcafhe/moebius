# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:39:26 2017
@author: Jérémie Fache
"""

from collections import namedtuple

from rx import Observable
from rx.internal import extensionmethod

_Structure = namedtuple('Structure', 'value, output')

class _Unique():
    pass

NO_SEED = _Unique


@extensionmethod(Observable)
def scan_map(self, selector, seed=NO_SEED):
    """
    Applies a selector function over two consecutive items from an observable
    sequence and returns result. The optional seed value is used as the initial
    value provided to the selector function.

    Examples
    ========

    Compute the difference between two consecutive items with no seed.

    >>> values = [1, 3, 6, 10]
    >>> rx.Observable.from_(values).scan_map(lambda last, new: new - last).subscribe(print)
    2
    3
    4

    >>> values = [1, 3, 6, 10]
    >>> rx.Observable.from_(values).scan_map(lambda last, new: new - last, seed=0).subscribe(print)
    1
    2
    3
    4

    """
    if seed is not NO_SEED:
        seed = _Structure(value=seed, output=None)

    def compare(last_structure, new_value):
        if last_structure is NO_SEED:
            result = NO_SEED
        else:
            result = selector(last_structure.value, new_value)
        return _Structure(value=new_value, output=result)

    pipeline = (self
                .scan(compare, seed=seed)
                .filter(lambda struct: struct.output is not NO_SEED)
                .map(lambda struct: struct.output)
                )

    return pipeline
