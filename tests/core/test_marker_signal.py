# -*- coding: utf-8 -*-

import numpy as np

import rx
import rx.testing

from moebius.core import markers
from moebius.bus.messages import (ready,
                                  combine_seeds)

from .testing import assert_message_equality_with_np


# -----------------------------------------------------------------------------
def test_enable():
    signals = np.arange(10 * 6).reshape((10, 6))
    sig_idx = 5
    sig = signals[sig_idx]
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_signal = markers.create_extract_signal(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_signal = ready('SIGNALS', signals).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_signal.seeds)

    obs = extract_signal(bm_status,
                         bm_signal_idx,
                         bm_signal
                         )

    expected_values = [ready('MARKER_SIGNAL#A', sig, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    for exp, act in zip(expected_values, actual_values):
        assert_message_equality_with_np(exp, act)


# -----------------------------------------------------------------------------
def test_disable_returns_empty_observable():
    signals = np.arange(10 * 6).reshape((10, 6))
    sig_idx = 5
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_signal = markers.create_extract_signal(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.DISABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_signal = ready('SIGNALS', signals).identify('Z')

    obs = extract_signal(bm_status,
                         bm_signal_idx,
                         bm_signal
                         )

    actual_values = []
    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert(len(actual_values) == 0)


# -----------------------------------------------------------------------------
def test_index_out_of_range_emits_NOT_AVAILABLE():
    signals = np.arange(10 * 6).reshape((10, 6))

    sig_idx = 10
    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_signal = markers.create_extract_signal(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_signal = ready('SIGNALS', signals).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_signal.seeds)

    actual_values = []
    expected_values = [ready('MARKER_SIGNAL#A', markers.NOT_AVAILABLE, seeds=seeds),
                             ]

    obs = extract_signal(bm_status,
                         bm_signal_idx,
                         bm_signal
                         )

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    for exp, act in zip(expected_values, actual_values):
        assert_message_equality_with_np(exp, act)
