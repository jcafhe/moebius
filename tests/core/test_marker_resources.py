# -*- coding: utf-8 -*-

import numpy as np

import rx
import rx.testing

from pyrsistent import (v as pv)

from moebius.core import markers
from moebius.core.api import (Resource,
                              FILE)

from moebius.bus.messages import (ready,
                                  combine_seeds)


# -----------------------------------------------------------------------------
def test_enable():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=('f0', 'f1', 'f2'),
                             ri= (0, 0, 0, 0, 1, 1, 1, 2, 2),
                             iir=(0, 1, 2, 3, 0, 1, 2, 0, 1),
                             ),
                    Resource(rtype=FILE,
                             rn=('single',),
                             ri= (0, 0, 0, 0, 0, 0, 0, 0, 0),
                             iir=(0, 1, 2, 3, 4, 5, 6, 7, 8),
                             ),
                    )

    sig_idx = 5
    expected = pv(Resource(rtype=FILE,
                           rn='f1',
                           ri=1,
                           iir=1,
                           ),
                  Resource(rtype=FILE,
                           rn='single',
                           ri=0,
                           iir=5,
                           ),
                  )

    mid = 'A'

    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_resources.seeds)

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    expected_values = [ready('MARKER_RESOURCES#A', expected, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (expected_values == actual_values)


# -----------------------------------------------------------------------------
def test_enable_with_np():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=np.array(('f0', 'f1', 'f2')),
                             ri= np.array((0, 0, 0, 0, 1, 1, 1, 2, 2)),
                             iir=np.array((0, 1, 2, 3, 0, 1, 2, 0, 1)),
                             ),
                    Resource(rtype=FILE,
                             rn=np.array(('single',)),
                             ri= np.array((0, 0, 0, 0, 0, 0, 0, 0, 0)),
                             iir=np.array((0, 1, 2, 3, 4, 5, 6, 7, 8)),
                             ),
                    )

    sig_idx = 5
    expected = pv(Resource(rtype=FILE,
                           rn='f1',
                           ri=1,
                           iir=1
                           ),
                  Resource(rtype=FILE,
                           rn='single',
                           ri=0,
                           iir=5
                           ),
                  )

    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_resources.seeds)

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    expected_values = [ready('MARKER_RESOURCES#A', expected, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (expected_values == actual_values)


# -----------------------------------------------------------------------------
def test_disable_emits_nothing():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=np.array(('f0', 'f1', 'f2')),
                             ri= np.array((0, 0, 0, 0, 1, 1, 1, 2, 2)),
                             iir=np.array((0, 1, 2, 3, 0, 1, 2, 0, 1)),
                             ),
                    Resource(rtype=FILE,
                             rn=np.array(('single',)),
                             ri= np.array((0, 0, 0, 0, 0, 0, 0, 0, 0)),
                             iir=np.array((0, 1, 2, 3, 4, 5, 6, 7, 8)),
                             ),
                    )

    sig_idx = 5
    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.DISABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    actual_values = []
    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (len(actual_values) == 0)

# -----------------------------------------------------------------------------
def test_iir_NOT_AVAILABLE():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=np.array(('f0', 'f1', 'f2')),
                             ri= np.array((0, 0, 0, 0, 1, 1, 1, 2, 2)),
                             iir=np.array((0, 1, 2, 3, 0,)),
                             ),
                    Resource(rtype=FILE,
                             rn=np.array(('single',)),
                             ri= np.array((0, 0, 0, 0, 0, 0, 0, 0, 0)),
                             iir=np.array((0, 1, 2, 3, 4,)),
                             ),
                    )

    sig_idx = 5
    expected = pv(Resource(rtype=FILE,
                           rn='f1',
                           ri=1,
                           iir=markers.NOT_AVAILABLE,
                           ),
                  Resource(rtype=FILE,
                           rn='single',
                           ri=0,
                           iir=markers.NOT_AVAILABLE,
                           ),
                  )

    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_resources.seeds)

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    expected_values = [ready('MARKER_RESOURCES#A', expected, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (expected_values == actual_values)

# -----------------------------------------------------------------------------
def test_ri_NOT_AVAILABLE():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=np.array(('f0', 'f1', 'f2')),
                             ri= np.array((0, 0, 0, 0, 1, )),
                             iir=np.array((0, 1, 2, 3, 0, 1, 2, 0, 1)),
                             ),
                    Resource(rtype=FILE,
                             rn=np.array(('single',)),
                             ri= np.array((0, 0, 0, 0, 0, )),
                             iir=np.array((0, 1, 2, 3, 4, 5, 6, 7, 8)),
                             ),
                    )

    sig_idx = 5
    expected = pv(Resource(rtype=FILE,
                           rn=markers.NOT_AVAILABLE,
                           ri=markers.NOT_AVAILABLE,
                           iir=1
                           ),
                  Resource(rtype=FILE,
                           rn=markers.NOT_AVAILABLE,
                           ri=markers.NOT_AVAILABLE,
                           iir=5
                           ),
                  )

    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_resources.seeds)

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    expected_values = [ready('MARKER_RESOURCES#A', expected, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (expected_values == actual_values)

# -----------------------------------------------------------------------------
def test_rn_NOT_AVAILABLE():
    # 9 points
    # 3 files
    ressources = pv(Resource(rtype=FILE,
                             rn=np.array(('f0', )),
                             ri= np.array((0, 0, 0, 0, 1, 1, 1, 2, 2)),
                             iir=np.array((0, 1, 2, 3, 0, 1, 2, 0, 1)),
                             ),
                    Resource(rtype=FILE,
                             rn=np.array(('single',)),
                             ri= np.array((0, 0, 0, 0, 0, 0, 0, 0, 0)),
                             iir=np.array((0, 1, 2, 3, 4, 5, 6, 7, 8)),
                             ),
                    )

    sig_idx = 5
    expected = pv(Resource(rtype=FILE,
                           rn=markers.NOT_AVAILABLE,
                           ri=1,
                           iir=1
                           ),
                  Resource(rtype=FILE,
                           rn='single',
                           ri=0,
                           iir=5
                           ),
                  )

    mid = 'A'
    scheduler = rx.testing.TestScheduler()
    extract_resources = markers.create_extract_resources(mid, scheduler)

    bm_status = markers.bm_status(mid, markers.ENABLE).identify('X')
    bm_signal_idx = markers.bm_signal_idx(mid, sig_idx).identify('Y')
    bm_resources = ready('RESOURCES', ressources).identify('Z')
    seeds = combine_seeds(bm_status.seeds,
                          bm_signal_idx.seeds,
                          bm_resources.seeds)

    obs = extract_resources(bm_status,
                            bm_signal_idx,
                            bm_resources
                            )

    expected_values = [ready('MARKER_RESOURCES#A', expected, seeds=seeds), ]
    actual_values = []

    obs.subscribe(lambda bm: actual_values.append(bm))
    scheduler.start()

    assert (expected_values == actual_values)
