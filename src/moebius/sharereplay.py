# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 21:19:30 2017
@author: Jérémie Fache
"""

import rx
from rx.internal import extensionmethod


@extensionmethod(rx.Observable)
def share_replay(self, buffer_size, window_size=None, scheduler=None):
    """
    Returns an observable sequence that shares a single subscription to the
    underlying sequence replaying notifications subject to a maximum time
    length for the replay buffer.

    This operator is a specialization of *replay()* which creates a
    subscription when the number of observers goes from zero to one,
    then shares that subscription with all subsequent observers until
    the number of observers returns to zero, at which point the
    subscription is disposed.

    example
    =======

    >>> var res = source.shareReplay(3)
    >>> var res = source.shareReplay(3, 500)
    >>> var res = source.shareReplay(3, 500, scheduler)

    signature
    =========

    .. function:: share_replay(buffer_size, window_size=None, scheduler=None)

       :param buffer_size: Maximum element count of the replay buffer.
       :param window_size: [Optional] Maximum time length of the replay buffer.
       :param scheduler: [Optional] Scheduler where connected observers within
                         the selector function will be invoked on.
       :type arg1: type description
       :type arg1: type description
       :return: An observable sequence that contains the elements
                of a sequence produced by multicasting the source sequence.
       :rtype: rx.Observable


   """
    return (self.replay(selector=None,
                        buffer_size=buffer_size,
                        window=window_size,
                        scheduler=scheduler)
                .ref_count()
                )





