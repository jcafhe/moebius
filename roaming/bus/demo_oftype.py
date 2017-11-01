# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 20:39:23 2017
@author: Jérémie Fache
"""

from proteus.bus import messages


def create_message(tag, status):
    return messages.BusMessage(tag=tag,
                               status=status,
                               payload=tag,
                               seeds=tag,
                               meta=tag)


type_0 = messages.oftype(tag='abc...')
m0 = create_message(tag='abc', status='some_status')

type_0(m0)
