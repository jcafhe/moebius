# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 18:53:18 2017
@author: Jérémie Fache
"""

from collections import namedtuple
import numpy as np

Ascan = namedtuple('Ascan', ['identifier',
                             'sensor',
                             'data',
                             'date',
                             'resources',  # iterable of Ressource
                             ]
                   )

Resource = namedtuple('Resource', ['rtype',  # ressources type
                                   'rn',  # resource names
                                   'ri',  # ressource indexes
                                   'iir',  # indexes in resource
                                   ]
                       )


Modifier = namedtuple('Modifier', 'name, short_description, full_description, function')


"""
Resource stream
===============

resources: iterable<Resource>

    <Resource>
        rn:  iterable <str>
        ri:  np.array <int>
        iir: np.array <int>

    <Resource>
        rn:  iterable <str>
        ri:  np.array <int>
        iir: np.array <int>

    ...



"""


def create_ascan(nrow=10, ncol=5):
#    nrow = 10
#    ncol = 5
    sig_count = nrow * ncol

    f0_Hz = 20
    f1_Hz = 40
    f2_Hz = 60

    smp_count = 200
    smp_rate_Hz = 100

    col_delays_smp = np.linspace(0.5, 0.0, ncol) * smp_count
    col_delays_smp = np.asarray(col_delays_smp, dtype=np.int)
    enveloppe = np.blackman(smp_count // 2)

    enveloppe_len = len(enveloppe)
    col_enveloppes = np.zeros((ncol, smp_count))

    for i in range(ncol):
        i_start = col_delays_smp[i]
        i_stop = i_start + enveloppe_len
        col_enveloppes[i, i_start:i_stop] = enveloppe

    period = 1 / smp_rate_Hz
    times = np.arange(smp_count) * period
    f0_sig = np.sin(2 * np.pi * f0_Hz * times)
    f1_sig = np.sin(2 * np.pi * f1_Hz * times)
    f2_sig = np.sin(2 * np.pi * f2_Hz * times)

    col_f1_amp = np.linspace(0.0, 1.0, num=ncol)
    row_f2_amp = np.linspace(0.0, 1.0, num=nrow)
    row_amp = np.linspace(0.1, 1.0, num=nrow)

    rows = []

    for i_row in range(nrow):
        amp = row_amp[i_row]
        f2_amp = row_f2_amp[i_row]

        row =[]
        for i_col in range(ncol):
            f1_amp = col_f1_amp[i_col]
            env_vector = col_enveloppes[i_col]

            signal = amp * env_vector * (f0_sig + f1_amp * f1_sig + f2_amp * f2_sig)
            row.append(signal.reshape((1, -1)))

        row_array = np.concatenate(row, axis=0)
        rows.append(row_array.reshape((1, ncol, smp_count)))


    data2d = np.concatenate(rows, axis=0)
    dataflatten = np.copy(data2d)
    dataflatten[1::2,:,:] = np.flip(dataflatten[1::2,:,:], axis=1)
    dataflatten = dataflatten.reshape((sig_count, smp_count))

    return data2d, dataflatten





