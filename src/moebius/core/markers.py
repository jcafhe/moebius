# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 19:23:11 2017
@author: Jérémie Fache
"""

from collections import namedtuple as _nt
import rx
from pyrsistent import (m as pm, freeze)
from moebius.bus.messages import (ready, READY, NO_SEED, combine_seeds, oftype)
from moebius.sharereplay import share_replay

MARKER_TRACK = 'MARKER_TRACK'
MARKER_UNTRACK = 'MARKER_UNTRACK'
MARKER_UNTRACK_ALL = 'MARKER_UNTRACK_ALL'
MARKER_UPDATE_SIGNAL_IDX = 'MARKER_UPDATE_SIGNAL_IDX'
MARKER_UPDATE_SAMPLE_IDX = 'MARKER_UPDATE_SAMPLE_IDX'

MARKER_SIGNAL = 'MARKER_SIGNAL'
MARKER_ENERGY = 'MARKER_ENERGY'
MARKER_RESOURCE = 'MARKER_RESSOURCE'
MARKER_FFT = 'MARKER_FFT'
MARKER_MOD_FFT = 'MARKER_MOD_FFT'
MARKER_MOD_SIGNAL = 'MARKER_MOD_SIGNAL'


# -----------------------------------------------------------------------------
def track(marker_id, seeds=NO_SEED):
    bm = ready(tag=MARKER_TRACK,
               payload=marker_id,
               seeds=seeds)
    return bm


# -----------------------------------------------------------------------------
def untrack(marker_id, seeds=NO_SEED):
    bm = ready(tag=MARKER_UNTRACK,
               payload=marker_id,
               seeds=seeds)
    return bm


# -----------------------------------------------------------------------------
def untrack_all(seeds=NO_SEED):
    bm = ready(tag=MARKER_UNTRACK_ALL,
               payload=None,
               seeds=seeds)
    return bm


# -----------------------------------------------------------------------------
def update_signal_idx(marker_id, signal_idx=None, seeds=NO_SEED):
    bm = ready(tag=MARKER_UPDATE_SIGNAL_IDX,
               payload=pm(marker_id=marker_id,
                          data=signal_idx
                          ),
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def update_sample_idx(marker_id, sample_idx=None, seeds=NO_SEED):
    bm = ready(tag=MARKER_UPDATE_SAMPLE_IDX,
               payload=pm(marker_id=marker_id,
                          data=sample_idx
                          ),
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def create_markers_pipeline(action8, signalsR8, energiesR8):
    marker_actionR8 = action8.filter(oftype('MARKER...', READY))

    signalsR8 = signalsR8.share_replay(1)
    energiesR8 = energiesR8.share_replay(1)

    trackR8 = marker_actionR8.filter(oftype(MARKER_TRACK))
    untrackR8 = marker_actionR8.filter(oftype(MARKER_UNTRACK))
    untrack_allR8 = marker_actionR8.filter(oftype(MARKER_UNTRACK_ALL))
    update_sig_idxR8 = marker_actionR8.filter(oftype(MARKER_UPDATE_SIGNAL_IDX))
    update_smp_idxR8 = marker_actionR8.filter(oftype(MARKER_UPDATE_SAMPLE_IDX))


    def create_single_marker_pipeline(trackR):
        NOT_AVAILABLE = None
#        print(trackR)
        marker_id = trackR.payload

        def test_for_marker_id(bm):
            return bm.payload.marker_id == marker_id

        this_untrackR8 = untrackR8.filter(lambda bm: marker_id == bm.payload)
        this_update_sig_idxR8 = update_sig_idxR8.filter(test_for_marker_id)
        this_update_smp_idxR8 = update_smp_idxR8.filter(test_for_marker_id)

        this_killerR8 = (rx.Observable
                         .merge(this_untrackR8,
                                untrack_allR8)
                         )

        # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        def extract_signal(update_sig_idxR, signalsR):
            seeds = combine_seeds(update_sig_idxR.seeds, signalsR.seeds)
            signals = signalsR.payload
            sig_idx = update_sig_idxR.payload.data

            try:
                data = signals[sig_idx]
            except IndexError:
                data = NOT_AVAILABLE
            return ready(tag=MARKER_SIGNAL,
                         payload=pm(marker_id=marker_id,
                                    data=data,
                                    ),
                         seeds=seeds,
                         )

        this_signal8 = (rx.Observable
                        .combine_latest(this_update_sig_idxR8, signalsR8, extract_signal)
                        .take_until(this_killerR8)
                        )

        # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        def extract_energy(update_sig_idxR, energiesR):
            seeds = combine_seeds(update_sig_idxR.seeds, energiesR.seeds)
            energies = energiesR.payload
            sig_idx = update_sig_idxR.payload.data

            try:
                data = energies[sig_idx]
            except IndexError:
                data = NOT_AVAILABLE

            return ready(tag=MARKER_ENERGY,
                         payload=pm(marker_id=marker_id,
                                    data=data,
                                    ),
                         seeds=seeds,
                         )

        this_energy8 = (energiesR8
                        .combine_latest(this_update_sig_idxR8, energiesR8, extract_energy)
                        .take_until(this_killerR8)
                        )

        # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        this_merged_data8 = (rx.Observable
                            .merge(this_signal8,
                                   this_energy8)
                            )
        return this_merged_data8

    # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    pipeline8 = (trackR8
                 .flat_map(create_single_marker_pipeline)

                 )
    return pipeline8

