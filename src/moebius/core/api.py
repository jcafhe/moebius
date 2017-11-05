# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 18:53:18 2017
@author: Jérémie Fache
"""

from collections import namedtuple

Ascan = namedtuple('Ascan', ['identifier',
                             'sensor',
                             'data',
                             'date',
                             'resources',  # iterable of Ressource
                             ]
                   )

Ressource = namedtuple('Resource', ['rtype',  # ressources type
                                    'rn',  # resource names
                                    'ri',  # ressource indexes
                                    'iir',  # indexes in resource
                                    ]
                       )

