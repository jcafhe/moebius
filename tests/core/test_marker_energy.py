# -*- coding: utf-8 -*-

import numpy as np

import rx
import rx.testing

import moebius.quantity as qty
from moebius.core import markers
from moebius.bus.messages import (ready,
                                  combine_seeds)

from .testing import assert_message_equality_with_np


# -----------------------------------------------------------------------------
def test_enable():
    energies = np.arange(10 * 6).reshape((10, 6))
    sig_idx = 5
    ene = energies[sig_idx]
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_energy = markers.create_extract_energy(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_energies = ready('ENERGY', qty.Scalar(energies)).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_energies.seeds)

    obs = extract_energy(bm_status,
                         bm_signal_idx,
                         bm_energies
                         )

    expected_values = [ready('MARKER_ENERGY#A', qty.Scalar(ene), seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    for exp, act in zip(expected_values, actual_values):
#        assert_message_equality_with_np(exp, act)
        assert (exp == act)

# -----------------------------------------------------------------------------
def test_disable_returns_empty_observable():
    energies = np.arange(10 * 6).reshape((10, 6))
    sig_idx = 5
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_energy = markers.create_extract_energy(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.DISABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_energies = ready('ENERGIES', qty.Scalar(energies)).identify('Z')

    obs = extract_energy(bm_status,
                         bm_signal_idx,
                         bm_energies
                         )

    actual_values = []
    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert(len(actual_values) == 0)


# -----------------------------------------------------------------------------
def test_index_out_of_range_emits_NOT_AVAILABLE():
    energies = np.arange(10 * 6).reshape((10, 6))

    sig_idx = 10
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_energy = markers.create_extract_energy(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_energies = ready('ENERGIES', qty.Scalar(energies)).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_energies.seeds)

    actual_values = []
    expected_values = [ready('MARKER_ENERGY#A', markers.NOT_AVAILABLE, seeds=seeds),
                             ]

    obs = extract_energy(bm_status,
                         bm_signal_idx,
                         bm_energies
                         )

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    for exp, act in zip(expected_values, actual_values):
        assert(exp == act)
