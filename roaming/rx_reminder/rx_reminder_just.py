# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 14:48:13 2017
@author: Jérémie Fache
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Nov  2 12:30:49 2017
@author: Jérémie Fache
"""

import rx
import logging
import time

log_format = "[%(threadName)s] %(message)s"
logging.basicConfig(format=log_format, level=logging.INFO)
logging.getLogger('rx').setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)

sub0 = rx.subjects.Subject()

stream0 = (sub0
           .observe_on(rx.concurrency.EventLoopScheduler())
           .scan(lambda c, _: c + 1, seed=-1)
           .map(lambda i: 's0 {}'.format(i))
           )


stream0.subscribe(lambda x: logger.info('stream0 <{}>'.format(x)))

just8 = (stream0
         .map(lambda item: rx.Observable.just(item).do_action(lambda x: logger.info('\t\tjust <{}>'.format(x))))
         .merge_all()
         )

just8.subscribe(lambda x: logger.info('\t\t\t\tmerged all <{}>'.format(x)))


def send_to_stream0():
    sub0.on_next(None)


print('just uses current_thread scheduler as default scheduler')

send_to_stream0()
send_to_stream0()

time.sleep(1.0)
