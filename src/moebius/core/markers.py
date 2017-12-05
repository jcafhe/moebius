# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 13:26:23 2017
@author: Jérémie Fache
"""

from collections import namedtuple as _nt
import numpy as np

import rx
from pyrsistent import (m as pm, v as pv, freeze)
from moebius.bus.messages import (ready, READY, NO_SEED, combine_seeds, oftype)
import moebius.quantity as qty
from . import api

# input tags
MARKER_SIGNAL_IDX = 'MARKER_SIGNAL_IDX'
MARKER_SAMPLE_IDX = 'MARKER_SAMPLE_IDX'
MARKER_STATUS = 'MARKER_STATUS'

# output tags
MARKER_SIGNAL = 'MARKER_SIGNAL'
MARKER_ENERGY = 'MARKER_ENERGY'
MARKER_RESOURCES = 'MARKER_RESOURCES'
MARKER_FFT = 'MARKER_FFT'
MARKER_MOD_FFT = 'MARKER_MOD_FFT'
MARKER_MOD_SIGNAL = 'MARKER_MOD_SIGNAL'

# status values
ENABLE = 'ENABLE'
DISABLE = 'DISABLE'


class __Unique():
    pass


# Object to describe a non available value
NOT_AVAILABLE = None  # __Unique()


# Marker id helper functions --------------------------------------------------
# -----------------------------------------------------------------------------
def append_marker_id(tag, marker_id):
    """
    Appends marker id to a bus message tag.
    """
    return tag + '#' + marker_id


# -----------------------------------------------------------------------------
def extract_marker_id(tag):
    """
    Extract marker id from a bus message tag.
    """
    return tag.split('#')[-1]


# -----------------------------------------------------------------------------
def oftype_with_id(marker_id, tag=None, status=None):
    # TODO : write unit tests
    legacy_oftype = oftype(tag, status)

    def inner(bm):
        bm_tag = bm.tag
        if '#' in bm_tag:
            li = bm_tag.split('#')
            if len(li) > 2:
                etext = ("Multiple '#' has been found in bus message tag. "
                         "This symbol is reserved for ids. Got {}".format(bm))
                raise ValueError(etext)

            matches_id = marker_id == extract_marker_id(bm_tag)
            return matches_id and legacy_oftype(bm._replace(tag=li[0]))

        else:
            return False

    return inner


# Bus Message helper functions ------------------------------------------------
# -----------------------------------------------------------------------------
def bm_signal_idx(marker_id, signal_idx=0, seeds=NO_SEED):
    """
    Helper function to create a bus message with tag MARKER_SIGNAL_IDX.
    """
    if signal_idx < 0:
        raise ValueError('signal_idx must be > 0. '
                         'Got {}'.format(signal_idx))

    tag = append_marker_id(MARKER_SIGNAL_IDX, marker_id)
    bm = ready(tag=tag,
               payload=signal_idx,
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def bm_sample_idx(marker_id, sample_idx=0, seeds=NO_SEED):
    """
    Helper function to create a bus message with tag MARKER_SAMPLE_IDX.
    """
    tag = append_marker_id(MARKER_SAMPLE_IDX, marker_id)
    bm = ready(tag=tag,
               payload=sample_idx,
               seeds=seeds,
               )
    return bm


# -----------------------------------------------------------------------------
def bm_status(marker_id, status, seeds=NO_SEED):
    """
    Helper function to create a bus message with tag MARKER_STATUS.
    """
    if status != ENABLE and status != DISABLE:
        raise ValueError('status must be {} or {}. '
                         'Got {}'.format(ENABLE, DISABLE, status))

    tag = append_marker_id(MARKER_STATUS, marker_id)
    bm = ready(tag=tag,
               payload=status,
               seeds=seeds,
               )
    return bm


# Pipeline creation functions -------------------------------------------------
# -----------------------------------------------------------------------------
def create_extract_signal(marker_id, scheduler=None):
    """
    returns a function returning an Observable to extract a signal
    from a data array for a specific marker id.

    .. function :: extract_signal(statusR, signal_idxR, signalsR)

       :param statusR: bus message [READY] holding the ENABLE/DISABLE
                       state of the current marker
       :param signal_idxR: bus message [READY] holding the signal index to
                           be used
       :param signalsR: bus message [READY] holding signals data array
       :return: rx.Observable
    """

    TAG = append_marker_id(MARKER_SIGNAL, marker_id)

    def inner(statusR, signal_idxR, signalsR):
        """
        .. function :: extract_signal(statusR, signal_idxR, signalsR)

           :param statusR: bus message [READY] holding the ENABLE/DISABLE
                           state of the current marker
           :param signal_idxR: bus message [READY] holding the signal index to
                               be used
           :param signalsR: bus message [READY] holding signals data array
           :return: rx.Observable
        """

        status = statusR.payload

        if status == DISABLE:
            return rx.Observable.empty()

        seeds = combine_seeds(signal_idxR.seeds, signalsR.seeds, statusR.seeds)
        sig_idx = signal_idxR.payload
        signals = signalsR.payload

        try:
            data = signals.value[sig_idx][:]
            data = qty.Scalar(data)
        except IndexError:
            data = NOT_AVAILABLE

        msg = ready(tag=TAG,
                    payload=data,
                    seeds=seeds,
                    )

        return (rx.Observable.just(value=msg, scheduler=scheduler))

    return inner


# -----------------------------------------------------------------------------
def create_extract_energy(marker_id, scheduler=None):
    """
    returns a function returning an Observable to extract a single energy
    value from a data array for a specific marker id.

    .. function :: extract_energy(statusR, signal_idxR, signalsR)

       :param statusR: bus message [READY] holding the ENABLE/DISABLE
                       state of the current marker
       :param signal_idxR: bus message [READY] holding the signal index to
                           be used
       :param energiesR: bus message [READY] holding energies data array
       :return: rx.Observable emitting 1 numerical value.
    """

    TAG = append_marker_id(MARKER_ENERGY, marker_id)

    def inner(statusR, signal_idxR, energiesR):
        """
        .. function :: extract_energy(statusR, signal_idxR, signalsR)

           :param statusR: bus message [READY] holding the ENABLE/DISABLE
                           state of the current marker
           :param signal_idxR: bus message [READY] holding the signal index to
                               be used
           :param energiesR: bus message [READY] holding energies data array
           :return: rx.Observable emitting 1 numerical value.
        """
        status = statusR.payload

        if status == DISABLE:
            return rx.Observable.empty()

        seeds = combine_seeds(signal_idxR.seeds,
                              energiesR.seeds,
                              statusR.seeds)

        sig_idx = signal_idxR.payload
        energies = energiesR.payload

        try:
            data = energies.value[sig_idx][:]
            data = qty.Scalar(data)
        except IndexError:
            data = NOT_AVAILABLE

        msg = ready(tag=TAG,
                    payload=data,
                    seeds=seeds,
                    )

        return (rx.Observable.just(value=msg, scheduler=scheduler))

    return inner


# -----------------------------------------------------------------------------
def create_extract_resources(marker_id, scheduler=None):
    """
    returns a function returning an Observable to extract resources related to
    a specific signal index for a specific marker id.

    .. function :: extract_resources(statusR, signal_idxR, resourcesR)

       :param statusR: bus message [READY] holding the ENABLE/DISABLE
                           state of the current marker
       :param signal_idxR: bus message [READY] holding the signal index to
                           be used
       :param resourcesR: bus message [READY] holding ressources data
       :return: rx.Observable emitting 1d ndarray
    """

    TAG = append_marker_id(MARKER_RESOURCES, marker_id)

    def inner(statusR, signal_idxR, resourcesR):
        """
        .. function :: extract_resources(statusR, signal_idxR, resourcesR)

           :param statusR: bus message [READY] holding the ENABLE/DISABLE
                               state of the current marker
           :param signal_idxR: bus message [READY] holding the signal index to
                               be used
           :param resourcesR: bus message [READY] holding ressources data
           :return: rx.Observable emitting 1d ndarray
        """
        # TODO : need implementation
        if statusR.payload == DISABLE:
            return rx.Observable.empty()

        seeds = combine_seeds(statusR.seeds,
                              signal_idxR.seeds,
                              resourcesR.seeds)

        src_resources = resourcesR.payload
        sig_idx = signal_idxR.payload

        rs = pv()
        for r in src_resources:
            rtype = r.rtype
            try:
                ri = r.ri[sig_idx]
            except IndexError:
                ri = NOT_AVAILABLE

            try:

                if ri is NOT_AVAILABLE:
                    rn = NOT_AVAILABLE
                else:
                    rn = r.rn[ri]

            except IndexError:
                rn = NOT_AVAILABLE

            try:
                iir = r.iir[sig_idx]
            except IndexError:
                iir = NOT_AVAILABLE

            res = api.Resource(rtype=rtype,
                               rn=rn,
                               ri=ri,
                               iir=iir,
                               )

            rs = rs.append(res)

        return rx.Observable.just(ready(tag=TAG, payload=rs, seeds=seeds))

    return inner


Spectrum = _nt('Spectrum', 'amplitudes, phases, frequencies')


# -----------------------------------------------------------------------------
def create_compute_fft(marker_id, scheduler=None):
    """
    returns a function returning an Observable to compute fft
    from a signal and a sampling rate for a specific marker id.

    .. function :: compute_fft(marker_signalR, sampling_rateR)

       :param marker_signalR: bus message [READY] holding the signal data
       :param sampling_rateR: bus message [READY] holding the sampling rate
       :return: rx.Observable emitting a Spertrum namedtuple
                with three isoshape 1d ndarray as amplitudes,
                phases, frequencies.
    """
    TAG = append_marker_id(MARKER_FFT, marker_id)

    def compute(signal, sampling_rate):
        sig = signal.value

        fft = np.fft.rfft(sig)
        amplitudes = np.abs(fft)
        phases = np.angle(fft)
        frequencies = sampling_rate * np.fft.rfftfreq(len(sig))

        return Spectrum(amplitudes=qty.Scalar(amplitudes),
                        phases=qty.Angle(phases, 'rad'),
                        frequencies=frequencies
                        )

    def inner(marker_signalR, sampling_rateR):
        """
        .. function :: compute_fft(marker_signalR, sampling_rateR)

           :param marker_signalR: bus message [READY] holding the signal data
           :param sampling_rateR: bus message [READY] holding the sampling rate
           :return: rx.Observable emitting a Spertrum namedtuple
                    with three isoshape 1d ndarray as amplitudes,
                    phases, frequencies.
        """

        sampling_rate = sampling_rateR.payload
#        sampling_rate_Hz = sampling_rate['Hz']
        signal = marker_signalR.payload

        if signal is NOT_AVAILABLE:
            return rx.Observable.empty()

        seeds = combine_seeds(marker_signalR.seeds,
                              sampling_rateR.seeds,
                              )

        return (rx.Observable
                .just(None, scheduler)
                .map(lambda _: compute(signal, sampling_rate))
                .map(lambda data: ready(tag=TAG, payload=data, seeds=seeds))
                )

    return inner


# -----------------------------------------------------------------------------
def create_markers(marker_ids,
                   action8,
                   signalsR8=None,
                   energiesR8=None,
                   resourcesR8=None,
                   positionsR8=None,
                   sampling_rateR8=None,
                   sensor_positionR8=None,
                   axis_compensationR8=None,
                   scheduler_provider=None):

    marker_actionR8 = (action8
                       .filter(oftype('MARKER...', READY))
                       )

    signalsR8 = signalsR8 or rx.Observable.empty()
    energiesR8 = energiesR8 or rx.Observable.empty()
    resourcesR8 = resourcesR8 or rx.Observable.empty()
    positionsR8 = positionsR8 or rx.Observable.empty()
    sampling_rateR8 = sampling_rateR8 or rx.Observable.empty()

    scheduler_provider = scheduler_provider or rx.concurrency

    def create_single_marker(marker_id):

        def test_for_marker_id(bm):
            bm_marker_id = extract_marker_id(bm.tag)
            return bm_marker_id == marker_id

        this_marker_actionR8 = marker_actionR8.filter(test_for_marker_id)

        this_sig_idxR8 = this_marker_actionR8.filter(oftype(MARKER_SIGNAL_IDX + '...'))
        this_smp_idxR8 = this_marker_actionR8.filter(oftype(MARKER_SAMPLE_IDX + '...'))
        this_statusR8 = this_marker_actionR8.filter(oftype(MARKER_STATUS + '...'))

        # SIGNAL ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        extract_signal = create_extract_signal(marker_id)
        this_signal8 = (rx.Observable
                        .combine_latest(this_statusR8,
                                        this_sig_idxR8,
                                        signalsR8,
                                        extract_signal)
                        .switch_latest()
                        .share()
                        )
        # FFT :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        compute_fft = create_compute_fft(marker_id)
        this_signalR8 = this_signal8.filter(oftype(status=READY))

        this_fft8 = (rx.Observable
                     .combine_latest(this_signalR8,
                                     sampling_rateR8,
                                     compute_fft)
                     .switch_latest()
                     )

        # ENERGY ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        extract_energy = create_extract_energy(marker_id)
        this_energy8 = (rx.Observable
                        .combine_latest(this_statusR8,
                                        this_sig_idxR8,
                                        energiesR8,
                                        extract_energy)
                        .switch_latest()
                        )

        # RESOURCE ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        extract_resource = create_extract_resources(marker_id)
        this_resources8 = (rx.Observable
                           .combine_latest(this_statusR8,
                                           this_sig_idxR8,
                                           resourcesR8,
                                           extract_resource)
                           .switch_latest()
                           )

        # :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        this_merged_data8 = rx.Observable.merge(this_signal8,
                                                this_fft8,
                                                this_energy8,
                                                this_resources8,
                                                )

        return this_merged_data8

#    ndigits = int(np.floor(np.log10(count))) + 1
#    mids = ['#{:0{ndigits}}'.format(i, ndigits=ndigits) for i in range(count)]
    obs = [create_single_marker(mid) for mid in marker_ids]
    print('create pipes for markers {}'.format(marker_ids))
    return rx.Observable.merge(obs)
