# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 20:28:06 2017
@author: Jérémie Fache
"""

from pyrsistent import (m as pm, v as pv)
import numpy as np

import rx
from moebius.bus import messages as msg
from moebius.core import api
from moebius.core.engine import Engine

nrow = 10
ncol = 6

ascan = api.Ascan(identifier='ascan#0',
                  sensor='tusht15',
                  data=np.arange(nrow * ncol).reshape((nrow, ncol)),
                  date='2017-11-03',
                  resources=pv())


bm = msg.ready(tag='engine/ASCAN_CHANGE', payload=ascan)

message8 = rx.Observable.just(bm)

engine = Engine(message8)
engine.output8.subscribe(print)


