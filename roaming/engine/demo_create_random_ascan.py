# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 18:14:55 2017
@author: Jérémie Fache
"""

import PIL
import numpy as np
import matplotlib.pyplot as plt
from moebius.core import api


data_uv, data_flat = api.create_ascan(100, 60)

energy_uv = np.sum(data_uv ** 2, axis=2)

img_size = data_uv.shape
norm_factor = 1 / np.max(energy_uv)
norm_energy_uv = energy_uv * norm_factor
im_energy_uv = PIL.Image.fromarray(np.uint8(energy_uv * norm_factor * 255.0))

plt.imshow(im_energy_uv)


