# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 13:50:08 2017
@author: Jérémie Fache
"""

import rx
import feedback
from pyrsistent import (s as ps)


def selector(last, new):
    r = new.difference(last)
    print('selector()>> last:{} new:{} diff:{}'.format(last, new, r))
    return r


set8 = rx.subjects.Subject()


#pipeline8 = (set8
#             .scan_map(selector, seed=ps())
##             .scan_map(selector)
#
#             )


#pipeline8.subscribe(lambda x: print('out ==> {}'.format(x)))

values = [1, 3, 6, 10]
rx.Observable.from_(values).scan_map(lambda last, new: new - last).subscribe(print)

#set8.on_next(ps(0, 1, 2))
#set8.on_next(ps(0, 5, 9, 1, 2, 3)) # adding 5, 9, 3



