# -*- coding: utf-8 -*-

import rx

# simulates a hot stream of values
ii = (rx.Observable
      .interval(500, scheduler=rx.concurrency.new_thread_scheduler)
      .share()
      )
ii.subscribe(lambda _: _)


# definition of different pipelines to be dynamically plugged in.
def pipeline_unity(obs):
    return obs


def pipeline_div_by_10(obs):
    return obs.map(lambda x: x / 10)


def pipeline_mul_by_10(obs):
    return obs.map(lambda x: x * 10)


pipelines = [pipeline_unity, pipeline_div_by_10, pipeline_mul_by_10]


# simulates a hot stream of pipelines to be dynamically plugged. It will loop
# over the pipelines list every 2s.
dynamic_pipelines = (rx.Observable
                     .interval(2000, scheduler=rx.concurrency.new_thread_scheduler)
                     .map(lambda i: i % len(pipelines))
                     .map(lambda i: pipelines[i])
                     .do_action(lambda p: print('working with pipeline: {}'.format(p)))
                     .share()
                     )

# use of switch_map to switch between piece of pipelines provided by
# the hot observable dynamic_pipelines
token = (dynamic_pipelines
         .switch_map(lambda pipe: pipe(ii))
         .subscribe(print)
         )

input('Press enter to exit ...\n')
token.dispose()

