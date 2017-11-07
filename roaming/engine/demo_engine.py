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
data = np.arange(nrow * ncol).reshape((nrow, ncol))

ascan = api.Ascan(identifier='ascan#0',
                  sensor='tusht15',
                  data=data,
                  date='2017-11-03',
                  resources=pv())


bm = msg.ready(tag='ASCAN', payload=data)

msgs = [bm,
        msg.ready('MARKER_ADD', 0),
        msg.ready('MARKER_ADD', 12),
        msg.ready('MARKER_ADD', -1),
        msg.ready('MARKER_REMOVE', 0),
        msg.ready('MARKER_CLEAR_ALL'),
        ]

message8 = rx.Observable.from_(msgs)

engine = Engine(message8)
engine.output8.subscribe(print)


