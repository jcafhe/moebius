# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 12:51:21 2017
@author: Jérémie Fache
"""

from collections import namedtuple as _nt
from collections.abc import Container
from pyrsistent import (m as pm, s as ps, freeze)


class BM(_nt('_Bm', 'tag, status, payload, seeds')):
    __slots__ = ()

    def identify(self, uid):
        """
        Returns a new message with updated seeds.
        Previous seeds (if any) are removed and the provided unique id is
        stored in the appropriate structure (i.e. seeds dict).
        """
        seeds = pm(**{self.tag: ps(uid)})
        return self._replace(seeds=seeds)


# alias for BusMessage
BusMessage = BM

READY = 'READY'
PROCESSING = 'PROCESSING'
ERROR = 'ERROR'

UNIDENTIFIED = 'UNIDENTIFIED'
UNIDENTIFIED_SEEDS = freeze({UNIDENTIFIED: ps()})

def ready(tag, payload=None, seeds=UNIDENTIFIED_SEEDS):
    """
    Returns a bus message with a READY status.
    """
    return BM(tag=tag,
              status=READY,
              payload=payload,
              seeds=seeds)


def processing(tag, ratio=None, meta=None, seeds=UNIDENTIFIED_SEEDS):
    """
    Returns a bus message with a PROCESSING status.

    ratio must be None or a tuple of the step that has just been processed, and
    the total number of steps.
    """
    payload = pm(ratio=ratio,
                 meta=meta)

    return BM(tag=tag,
              status=PROCESSING,
              payload=payload,
              seeds=seeds)


def error(tag, ex, seeds=UNIDENTIFIED_SEEDS):
    return BM(tag=tag,
              status=ERROR,
              payload=ex,
              seeds=seeds)

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def oftype(tag=None, status=None):
    """
    Returns a function that tests for a specific type of Bus Message.

    Return a test function that takes as input a Bus Message and returns a
    boolean. *tag* and *status* arguments specify the type of message for
    which the function returns True. These arguments can be None (i.e. no
    tests will be performed for that argument). Ellipsis can be used only with
    tag argument as a 'startswith' meaning.

    *tag* and *status* support single value as well as an iterable.

    This function is designed to be used with rx.Observable.filter().

    Examples:
    --------

    Definition of a list of messages to be sequencially emitted.

    >>> messages = [BusMessage('A', 'STARTED', 0, {}),
                    BusMessage('A', 'PROCESSING', 1, {}),
                    BusMessage('A', 'PROCESSING', 2, {}),
                    BusMessage('B', 'STARTED', 3, {}),
                    BusMessage('C', 'READY', 4, {}),
                    BusMessage('A', 'PROCESSING', 5, {}),
                    BusMessage('CC', 'PROCESSING', 5, {})]

    Filtering messages with tag 'A' and status 'PROCESSING'.

    >>> rx.Observable.from_(messages).filter(oftype('A', 'PROCESSING')).subscribe(print)
    BM(tag='A', status='PROCESSING', payload=1, seeds={})
    BM(tag='A', status='PROCESSING', payload=2, seeds={})
    BM(tag='A', status='PROCESSING', payload=5, seeds={})

    Filtering with multiple tags ("A" and "B"). This will discard messages
    with tag 'C' and 'CC'.

    >>> tags = ('A', 'B')
    >>> rx.Observable.from_(messages).filter(oftype(tags)).subscribe(print)
    BM(tag='A', status='STARTED', payload=0, seeds={})
    BM(tag='A', status='PROCESSING', payload=1, seeds={})
    BM(tag='A', status='PROCESSING', payload=2, seeds={})
    BM(tag='B', status='STARTED', payload=3, seeds={})
    BM(tag='A', status='PROCESSING', payload=5, seeds={})

    Filtering with ellipsis 'C...' will only pass messages with tag starting
    with 'C' (i.e. 'C' and 'CC').

    >>> rx.Observable.from_(messages).filter(oftype('C...')).subscribe(print)
    BM(tag='C', status='READY', payload=4, seeds={})
    BM(tag='CC', status='PROCESSING', payload=5, seeds={})
    """

    mtags = tag
    mstatus = status

    match_tag = _match_tag(mtags)
    match_status = _match_status(mstatus)

    def inner(bm):
        try:
            tag = bm.tag
            status = bm.status
        except AttributeError:
            etext = ("{} object to be tested against tags:{} status:{} is "
                     "not compatible with the bus.BusMessage interface. "
                     "Got type:{} object:{}"
                     ).format('bus.oftype()',
                              mtags,
                              mstatus,
                              type(bm),
                              bm)

            raise TypeError(etext)

        return match_tag(tag) and match_status(status)
    return inner


# -----------------------------------------------------------------------------
def _to_tuple(x):
    if isinstance(x, Container) and not isinstance(x, str):
        return tuple(x)
    return (x,)


# -----------------------------------------------------------------------------
def _match_tag(mtags):
    if mtags is None:
        return lambda tag: True

    mtags = _to_tuple(mtags)

    # differentiates requested tags with ellipsis
    startswith_mtags = []
    exact_mtags = []

    for tag in mtags:
        if tag.find('...') == -1:
            exact_mtags.append(tag)
        else:
            startswith_mtag = tag.split('...')[0]
            startswith_mtags.append(startswith_mtag)

    def in_startswith_mtags(tag):
        for mtag in startswith_mtags:
            if tag.startswith(mtag):
                return True
        return False

    return lambda tag: tag in exact_mtags or in_startswith_mtags(tag)


# -----------------------------------------------------------------------------
def _match_status(mstatus):
    if mstatus is None:
        return lambda tag: True

    exact_status = _to_tuple(mstatus)

    return lambda sta: sta in exact_status


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def combine_seeds(*args):
    """Combines multiples seeds and returns a seeds map.
    """
    seedss = args
    result = pm()

    for seeds in seedss:
        if seeds is not None:
            result = result.update_with(lambda vec, val: vec | val, seeds)

    return result


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
def propagates_seeds():
    """
    wrapping function to propagates and combines seeds from one or
    multiple streams of BusMessages.

    The returned function takes as input one or multiple rx.Observables
    emitting BusMessages, forwards messages with
    *READY* status to the
    decorated function and updates seeds of messages emitted by the
    decorated function.

    Note: the decorated function must returns an rx.Observable of BusMessage.
    """
    def inner(*args, **kwargs):
        pass

    raise NotImplementedError



