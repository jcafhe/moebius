# -*- coding: utf-8 -*-

import pytest
import numpy as np

from moebius.core import markers
from moebius.bus.messages import (ready, error,
                                  combine_seeds)


# -----------------------------------------------------------------------------
def test_not_a_marker_message():
    message = ready('MESSAGE', 12)
    oftype = markers.oftype_with_id('id0', message.tag, message.status)
    assert(oftype(message) == False)


# -----------------------------------------------------------------------------
def test_multiple_ids_in_tag_raises_ValueError():
    tag = markers.append_marker_id('TAG', 'id0')
    tag = markers.append_marker_id(tag, 'id1')
    message = ready(tag, 12)
    oftype = markers.oftype_with_id('id0', message.tag, message.status)

    with pytest.raises(ValueError):
        oftype(message)


# -----------------------------------------------------------------------------
def test_right_id():
    tag = markers.append_marker_id('TAG', 'id0')
    message = ready(tag, 12)
    oftype = markers.oftype_with_id('id0')

    assert(oftype(ready(tag, 12)))
    assert(oftype(error(tag, 12)))
    assert(not oftype(ready(markers.append_marker_id('TAG', 'id1'), 12)))
