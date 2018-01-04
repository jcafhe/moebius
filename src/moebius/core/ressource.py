# -*- coding: utf-8 -*-
from collections import namedtuple as _namedtuple
import h5py as _h5py

FILE = 'FILE'

Resource = _namedtuple('Resource',
                       ['rtype',  # ressources type
                        'rn',     # resource names
                        'ri',     # ressource indexes
                        'iir',    # indexes in resource
                        ]
                       )


# -----------------------------------------------------------------------------
def save_ressource_to_file(path, res):
    with _h5py.File(path, mode='w') as file:

        file.attrs['rtype'] = res.rtype

        rn = res.rn
        dt = _h5py.special_dtype(vlen=str)
        rn_set = file.create_dataset('rn', shape=(len(rn),), dtype=dt)
        rn_set[:] = rn

        file.create_dataset('ri', data=res.ri)
        file.create_dataset('iir', data=res.iir)


# -----------------------------------------------------------------------------
def load_ressource_from_file(path):
    with _h5py.File(path, mode='r') as file:
        rtype = file.attrs['rtype']
        rn = file['rn'][:]
        ri = file['ri'][:]
        iir = file['iir'][:]

    return Resource(rtype=rtype, rn=rn, ri=ri, iir=iir)


# -----------------------------------------------------------------------------
def save_scan_to_file(path, data):
    with _h5py.File(path, mode='w') as file:
        file.create_dataset('data', data=data)


# -----------------------------------------------------------------------------
def load_scan_from_file(path):
    with _h5py.File(path, mode='r') as file:
        data = file['data'][:]

    return data
