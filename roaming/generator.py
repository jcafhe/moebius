# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 13:30:20 2017
@author: Jérémie Fache
"""
import rx
import time
import logging
log_format = '[%(threadName)s]%(message)s'
logging.basicConfig(format=log_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

obj0 = [0, 1, 2]

class Iterator():
    def __init__(self, obj):
        self._obj = obj
        self._idx = 0
        self._count = len(obj)

    def __iter__(self):
        return self

    def __next__(self):
        if self._idx < self._count:
            logging.debug('next ids: {}'.format(self._idx))
            value = self._obj[self._idx]
            self._idx += 1
            return value
        else:
            raise StopIteration()


class Iterable():
    def __init__(self, obj):
        self._obj = obj

    def __iter__(self):
        return Iterator(self._obj)
#        return self

#        def inner():
#            for value in self._obj:
#                yield value
#
#        return inner

obj = Iterable(obj0)
#
for v in obj.__iter__():
    print(v)
