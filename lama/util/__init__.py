import typing as t
import numpy as np

__version__ = '0.1.0'
__all__ = ["StreamerBuilder", "decorators",
           "to_dictionary", "identity", "to_list",
           "to_tuple", "to_set", "to_narray"]


def to_dictionary(iterator, key_mapper=lambda it: it[0],
                  values_mapper=lambda it: it[1]):
    return {key_mapper(it): values_mapper(it) for it in iterator}


def identity(t):
    return t


def to_list(iterator):
    return list(iterator)


def to_tuple(iterator):
    return tuple(iterator)


def to_set(iterator):
    return set(iterator)


def to_ndarray(iterator, dtpye):
    return np.asarray(list(iterator), dtpye)
