# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 22:28:41 2017
@author: Jérémie Fache
"""

import rx


action8 = rx.subjects.Subject()


def memo(x):
    return rx.Observable.defer(lambda: rx.Observable.just(x))

pipeline = (action8
            .defer(lambda x: rx.Observable.just(x))
            )


out_A = pipeline.subscribe(lambda x: print('out_A {}'.format(x)))



action8.on_next(0)
action8.on_next(1)
out_B = pipeline.subscribe(lambda x: print('out_B {}'.format(x)))

action8.on_next(2)
action8.on_next(3)
