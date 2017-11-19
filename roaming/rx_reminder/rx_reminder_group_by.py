# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:31:58 2017
@author: Jérémie Fache
"""

import rx

values = (rx.Observable
            .from_([0, 1, 2, 0])
            )

def do_something_with_group(group):
    key = group.key
    print('create group[{}]'.format(key))
    return group

def duration_selector(group):
    key = group.key
    print('defining duration of group[{}]'.format(key))
    return rx.Observable.never()

token = (values
         .group_by_until(key_selector=lambda v: v,
                         element_selector=None,
                         duration_selector=duration_selector)
         .map(do_something_with_group)
         .merge_all()
         .subscribe(lambda x: print('received {}'.format(x)))
         )

