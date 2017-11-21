# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:26:23 2017
@author: Jérémie Fache
"""

from collections import namedtuple as _nt
import numpy as np

import rx
from pyrsistent import (m as pm, v, freeze)
from moebius.bus.messages import (ready, READY, NO_SEED, combine_seeds, oftype)
from moebius.sharereplay import share_replay
from . import api

MARKER_SIGNAL_IDX = 'MARKER_SIGNAL_IDX'
MARKER_SAMPLE_IDX = 'MARKER_SAMPLE_IDX'
MARKER_STATUS = 'MARKER_STATUS'


MARKER_SIGNAL = 'MARKER_SIGNAL'
MARKER_ENERGY = 'MARKER_ENERGY'
MARKER_RESOURCE = 'MARKER_RESSOURCE'
MARKER_FFT = 'MARKER_FFT'
MARKER_MOD_FFT = 'MARKER_MOD_FFT'
MARKER_MOD_SIGNAL = 'MARKER_MOD_SIGNAL'

ENABLE = 'ENABLE'
DISABLE = 'DISABLE'
NOT_AVAILABLE = 'NOT_AVAILABLE'
"""
examples:

MARKER_SAMPLE_IDX/#003
MARKER_SIGNAL/#010

"""


# -----------------------------------------------------------------------------
def bm_signal_idx(marker_id, signal_idx=0, seeds=NO_SEED):
    if signal_idx < 0:
        raise ValueError('signal_idx must be > 0. '
                         'Got {}'.format(signal_idx))

    bm = ready(tag=MARKER_SIGNAL_IDX + '/' + marker_id,
               payload=signal_idx,
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def bm_sample_idx(marker_id, sample_idx=0, seeds=NO_SEED):
    bm = ready(tag=MARKER_SAMPLE_IDX + '/' + marker_id,
               payload=sample_idx,
               seeds=seeds,
               )
    return bm

# -----------------------------------------------------------------------------
def bm_status(marker_id, status, seeds=NO_SEED):
    if status != ENABLE and status != DISABLE:
        raise ValueError('status must be {} or {}. '
                         'Got {}'.format(ENABLE, DISABLE, status))

    bm = ready(tag=MARKER_STATUS + '/' + marker_id,
               payload=status,
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def compute_fft(signal, sampling_rate_Hz):
    fft = np.fft.rfft(signal)
    amplitudes = np.abs(fft)
    phases = np.angle(fft)
    frequencies = sampling_rate_Hz * np.fft.rfftfreq(len(signal))
    return _nt('FFT', 'amplitudes, phases, frequencies')(amplitudes,
                                                         phases,
                                                         frequencies)


# -----------------------------------------------------------------------------
def create_markers(count,
                   action8,
                   signalsR8=None,
                   energiesR8=None,
                   resourcesR8=None,
                   positionsR8=None,
                   sampling_rateR8=None,
                   scheduler_provider=None):

    marker_actionR8 = action8.filter(oftype('MARKER...', READY))

    if signalsR8 is None:
        signalsR8 = rx.Observable.empty()
    else:
        signalsR8 = signalsR8.share_replay(1)

    if energiesR8 is None:
        energiesR8 = rx.Observable.empty()
    else:
        energiesR8 = energiesR8.share_replay(1)

    if resourcesR8 is None:
        resourcesR8 = rx.Observable.empty()
    else:
        resourcesR8 = resourcesR8.share_replay(1)

    if positionsR8 is None:
        positionsR8 = rx.Observable.empty()
    else:
        positionsR8 = positionsR8.share_replay(1)

    if sampling_rateR8 is None:
        sampling_rateR8 = rx.Observable.empty()
    else:
        sampling_rateR8 = sampling_rateR8.share_replay(1)

    scheduler_provider = scheduler_provider or rx.concurrency


    def create_single_marker(marker_id):
        SUFFIX = '/{}'.format(marker_id)

        def test_for_marker_id(bm):
            bm_marker_id = bm.tag.split('/')[-1]
            return bm_marker_id == marker_id

        this_marker_actionR8 = marker_actionR8.filter(test_for_marker_id)

        this_sig_idxR8 = this_marker_actionR8.filter(oftype(MARKER_SIGNAL_IDX + '...'))
        this_smp_idxR8 = this_marker_actionR8.filter(oftype(MARKER_SAMPLE_IDX + '...'))
        this_statusR8 = this_marker_actionR8.filter(oftype(MARKER_STATUS + '...'))

        # SIGNAL ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        def extract_signal(sig_idxR, signalsR):
            seeds = combine_seeds(sig_idxR.seeds, signalsR.seeds)
            signals = signalsR.payload
            sig_idx = sig_idxR.payload

            try:
                data = signals[sig_idx]
            except IndexError:
                data = NOT_AVAILABLE

            return ready(tag=MARKER_SIGNAL + SUFFIX,
                         payload=data,
                         seeds=seeds,
                         )

        this_signal8 = (rx.Observable
                        .combine_latest(this_sig_idxR8, signalsR8, extract_signal)
                        )

        this_signalR8 = this_signal8.filter(oftype(status=READY))

        # FFT :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        def fft_pipe(sigR, srR):
            seeds = combine_seeds(sigR.seeds, srR.seeds)
            sig = sigR.payload.data
            sr = srR.payload
            if sig is NOT_AVAILABLE:
                return (rx.Observable
                        .just(ready(tag=MARKER_FFT + SUFFIX,
                                    payload=NOT_AVAILABLE,
                                    seeds=seeds)
                              )
                        )

            return (rx.Observable
                    .just(0, scheduler_provider.thread_pool_scheduler)
                    .map(lambda _: compute_fft(sig, sr))
                    .map(lambda fft: ready(tag=MARKER_FFT + SUFFIX, payload=fft, seeds=seeds))
                    )

        this_fft8 = (rx.Observable
                     .combine_latest(this_signalR8, sampling_rateR8, fft_pipe)
                     .switch_latest()
                     )

        # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        this_merged_data8 = rx.Observable.merge(this_signal8,
                                                this_fft8,
#                                                this_energy8,
#                                                this_resource8
                                                )

        return this_merged_data8



    ndigits = int(np.floor(np.log10(count))) + 1
    mids = ['#{:0{ndigits}}'.format(i, ndigits=ndigits) for i in range(count)]
    obs = [create_single_marker(mid) for mid in mids]
    print(mids)
    return rx.Observable.merge(obs)

