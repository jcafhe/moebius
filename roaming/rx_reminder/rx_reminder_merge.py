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
sub1 = rx.subjects.Subject()

stream0 = (sub0
           .observe_on(rx.concurrency.EventLoopScheduler())
           .scan(lambda c, _: c + 1, seed=-1)
           .map(lambda i: 's0 {}'.format(i))
           )

stream1 = (sub1
           .observe_on(rx.concurrency.EventLoopScheduler())
           .scan(lambda c, _: c + 1, seed=-1)
           .map(lambda i: 's1 {}'.format(i))
           )

stream0.subscribe(lambda x: logger.info('stream0 "{}"'.format(x)))
stream1.subscribe(lambda x: logger.info('stream1 "{}"'.format(x)))

mrg_stream = rx.Observable.merge(stream0, stream1)
mrg_stream.subscribe(lambda x: logger.info('\t\t\tmerged "{}"'.format(x)))


def send_to_stream0():
    sub0.on_next(None)


def send_to_stream1():
    sub1.on_next(None)

print('merge uses immediate scheduler as default')

send_to_stream0()
send_to_stream0()

send_to_stream1()
send_to_stream0()

send_to_stream1()

time.sleep(1.0)
