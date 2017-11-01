# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 19:39:20 2017
@author: Jérémie Fache
"""

import pytest
from collections import namedtuple
from moebius.bus import messages

def create_message(tag, status):
    return messages.BusMessage(tag=tag,
                               status=status,
                               payload=tag,
                               seeds=tag)


# -----------------------------------------------------------------------------
def test_raise_TypeError_when_no_tag_attrib():

    filt = messages.oftype('abc...', 'stat0')
    with pytest.raises(TypeError):
        filt(namedtuple('M', 'bar, foo')(bar='abc', foo='cde'))

    filt = messages.oftype('abc...', None)
    with pytest.raises(TypeError):
        filt(namedtuple('M', 'bar')(bar='abc'))



def test_raise_TypeError_when_no_status_attrib():

    filt = messages.oftype('abc...', 'stat0')
    with pytest.raises(TypeError):
        filt(namedtuple('M', 'tag, foo')(tag='abc', foo='cde'))

    filt = messages.oftype('abc...', None)
    with pytest.raises(TypeError):
        filt(namedtuple('M', 'tag')(tag='abc'))



# -----------------------------------------------------------------------------
def test_tag_only():
    m = [create_message('A', 'status0'),
         create_message('B', 'status1'),
         create_message('AA', 'status2'),
         create_message('B', 'A'),
         ]

    type_A = messages.oftype('A')

    assert(type_A(m[0]) == True)
    assert(type_A(m[1]) == False)
    assert(type_A(m[2]) == False)
    assert(type_A(m[3]) == False)

# -----------------------------------------------------------------------------
def test_tag_only_with_ellipsis():
    m = [create_message('abc', 'status0'),
         create_message('def', 'status1'),
         create_message('abcdef', 'status2'),
         create_message('B', 'abcdef'),
         create_message('ab', 'status2'),
         ]

    type_A = messages.oftype(tag='abc...')

    assert(type_A(m[0]) == True)
    assert(type_A(m[1]) == False)
    assert(type_A(m[2]) == True)
    assert(type_A(m[3]) == False)
    assert(type_A(m[4]) == False)

# -----------------------------------------------------------------------------
def test_tags_only_with_some_with_ellipsis():

    type_A = messages.oftype(tag=('abc...', 'Bb', 'cd...'))

    assert(type_A(create_message('x', 'ab')) == False)
    assert(type_A(create_message('ab', 'status0')) == False)
    assert(type_A(create_message('abc', 'status0')) == True)
    assert(type_A(create_message('abcd', 'status1')) == True)
    assert(type_A(create_message('abcde', 'status2')) == True)
    assert(type_A(create_message('B', 'abcdef')) == False)
    assert(type_A(create_message('Bb', 'abcdef')) == True)
    assert(type_A(create_message('BB', 'abcdef')) == False)
    assert(type_A(create_message('Bbb', 'abcdef')) == False)
    assert(type_A(create_message('c', 'status2')) == False)
    assert(type_A(create_message('cd', 'status2')) == True)
    assert(type_A(create_message('cde', 'status2')) == True)
    assert(type_A(create_message('cdef', 'status2')) == True)
    assert(type_A(create_message('x', 'cd...')) == False)

# -----------------------------------------------------------------------------
def test_status_only():
    m = [create_message('A', 'status0'),
         create_message('B', 'status1'),
         create_message('AA', 'status2'),
         create_message('status2', 'A'),
         ]

    type_status1 = messages.oftype(status='status1')

    assert(type_status1(m[0]) == False)
    assert(type_status1(m[1]) == True)
    assert(type_status1(m[2]) == False)
    assert(type_status1(m[3]) == False)


# -----------------------------------------------------------------------------
def test_multiple_tags_and_status():
    type_A = messages.oftype(tag=('abc...', 'Bb', 'cd...'),
                             status=('PROC','ERROR'))

    assert(type_A(create_message('x', 'ab')) == False)
    assert(type_A(create_message('ab', 'status0')) == False)
    assert(type_A(create_message('abc', 'status0')) == False)

    assert(type_A(create_message('abc', 'PROC')) == True)
    assert(type_A(create_message('abcd', 'ERROR')) == True)
    assert(type_A(create_message('abcd', 'FOO')) == False)
    assert(type_A(create_message('abcde', 'PROC')) == True)

    assert(type_A(create_message('B', 'abcdef')) == False)
    assert(type_A(create_message('Bb', 'abcdef')) == False)
    assert(type_A(create_message('Bb', 'ERROR')) == True)
    assert(type_A(create_message('BB', 'PROC')) == False)
    assert(type_A(create_message('Bbb', 'abcdef')) == False)

    assert(type_A(create_message('c', 'ERROR')) == False)
    assert(type_A(create_message('cd', 'ERROR')) == True)
    assert(type_A(create_message('cde', 'PROC')) == True)
    assert(type_A(create_message('cdef', 'FOO')) == False)
    assert(type_A(create_message('PROC', 'cd')) == False)




