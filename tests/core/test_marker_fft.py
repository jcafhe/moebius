# -*- coding: utf-8 -*-

import numpy as np

import rx
import rx.testing

from moebius.quantity import (Frequency, Scalar, Angle, Time)
from moebius.core import markers
from moebius.bus.messages import (ready,
                                  combine_seeds)

from .testing import assert_message_equality_with_np


def compute(signal, sampling_rate):
    sig = signal.value
    fft = np.fft.rfft(sig)
    amplitudes = np.abs(fft)
    phases = np.angle(fft)
    frequencies = sampling_rate * np.fft.rfftfreq(len(sig))
    return markers.Spectrum(amplitudes=Scalar(amplitudes),
                            frequencies=frequencies,
                            phases=Angle(phases, 'rad'))


# -----------------------------------------------------------------------------
def test_computation():
    sampling_rate = Frequency(100, 'Hz')
    times = Time(np.linspace(0.0, 1.0, sampling_rate['Hz']), 's')
    signal = Scalar(np.sin(2 * np.pi * 2.0 * times['s']))
    fft = compute(signal, sampling_rate)

    # freq = 2 Hz
    # length = 1s
    # count = 100 pts
    # step = 10ms
    # sr = 100 Hz

    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    compute_fft = markers.create_compute_fft(mid, scheduler)

    bm_sampling_rate = ready('SAMPLING_RATE', sampling_rate).identify('Y')
    bm_signal = ready('SIGNAL', signal).identify('Z')

    seeds = combine_seeds(bm_sampling_rate.seeds,
                          bm_signal.seeds)

    obs = compute_fft(marker_signalR=bm_signal,
                      sampling_rateR=bm_sampling_rate,
                      )

    expected_values = [ready('MARKER_FFT#A', fft, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    for exp, act in zip(expected_values, actual_values):
        assert (expected_values == actual_values)


# -----------------------------------------------------------------------------
def test_NOT_AVAILABLE_SIGNAL_returns_empty_observable():

    sampling_rate = Frequency(100, 'Hz')
    signal = markers.NOT_AVAILABLE

    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    compute_fft = markers.create_compute_fft(mid, scheduler)

    bm_sampling_rate = ready('SAMPLING_RATE', sampling_rate).identify('Y')
    bm_signal = ready('SIGNAL', signal).identify('Z')

    obs = compute_fft(marker_signalR=bm_signal,
                      sampling_rateR=bm_sampling_rate,
                      )


    actual_values = []
    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert(len(actual_values) == 0)