# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 09:20:32 2017
@author: Jérémie Fache
"""

import numpy as np

path = 'C:\\DEV\\toto.npy'
data = np.arange(20 * 6).reshape((20, 6))

def create_file(path, data):
    np.save(path, data)


def read_file(path):
    fp = np.lib.format.open_memmap(filename=path,
                                   mode='r',
                                   )
    print(fp)


