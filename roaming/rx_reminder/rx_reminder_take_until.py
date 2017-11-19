# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 12:53:06 2017
@author: Jérémie Fache
"""

import rx
import time

message8 = rx.Observable.interval(500, scheduler=rx.concurrency.new_thread_scheduler).share()
cancel8 = rx.subjects.Subject()

pipeline = (message8
            .map(lambda x: x)
            .take_until(cancel8)
            )
pipeline.subscribe(on_next=lambda v: print('on_next: {}'.format(v)),
                   on_error=lambda e: print('on_error: {}'.format(e)),
                   on_completed=lambda: print('on_completed')
                   )

print('Pushing')


time.sleep(3.0)
print('cancelling')
cancel8.on_next(None)

time.sleep(3.0)
print('finishing')