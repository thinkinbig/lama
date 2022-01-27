from __future__ import annotations
import copy
import typing as t

import numpy as np

from lama.util.decorators import suppress

T = t.TypeVar('T')
U = t.TypeVar('U')
V = t.TypeVar('V')
It = t.TypeVar('It', bound=t.Iterator)


def to_dictionary(iterator: It[T], key_mapper: t.Callable[[T], V] = lambda it: it[0],
                  values_mapper: t.Callable[[T], U] = lambda it: it[1]) -> t.Dict[V, U]:
    return {key_mapper(it): values_mapper(it) for it in iterator}


def identity(t: T) -> T:
    return t


def to_list(iterator: It[T]) -> t.List[T]:
    return list(iterator)


def to_tuple(iterator: It[T]) -> t.Tuple[T]:
    return tuple(iterator)


def to_set(iterator: It[T]) -> t.Set[T]:
    return set(iterator)


def to_ndarray(iterator: It[T], dtpye) -> np.narray[T]:
    return np.asarray(list(iterator), dtpye)


class StreamerBuilder(t.Generic[T]):
    """
    StreamerBuilder is a wrapper class to wrap iterator and
    support chaining functions to make code more readable.

    The merit of implementing this class is that the functions won't
    be actually invoked until it is collected or consumed.
    """

    def __init__(self, iterator: It[T]):
        if not isinstance(iterator, t.Iterable):
            raise Exception("Streamer Builder must accept an Iterable")
        self._iterator = iterator
        self._callbacks = []

    @staticmethod
    def build(iterator: It[T]) -> StreamerBuilder:
        return StreamerBuilder(iterator)

    def map(self, f: t.Callable[[T], U]) -> StreamerBuilder:
        """
        Maps every unit in Iterator with function

        """

        def _mapper(iterator: It[T]) -> It[U]:
            for data in iterator:
                yield f(data)

        self._register_callback(_mapper)
        return self

    def filter(self, f: t.Callable[[T], bool]) -> StreamerBuilder:
        def _filter(iterator: t.Iterable[T]):
            for data in iterator:
                if f(data):
                    yield data

        self._register_callback(_filter)
        return self

    @suppress(excepts=StopIteration)
    def reduce(self, f: t.Callable[[T, U], T]) -> It[T]:
        def _reduce(iterable: t.Iterable[T]):
            _iterator = self._to_iterator(iterable)
            value = next(_iterator)
            for data in _iterator:
                value = f(value, data)
            return value
        self._register_callback(_reduce)
        return self

    def split(self, spliter: t.Callable[[T], It[T]]) -> It[T]:
        def _split(iterator: t.Iterable[T]):
            _res = []
            for data in iterator:
                for response in spliter(data):
                    _res.append(response)
            return iter(_res)
        self._register_callback(_split)
        return self

    def _register_callback(self, callback: t.Callable[..., t.Iterable[T]]):
        self._callbacks.append(callback)

    def collect(self, fun: t.Callable[[It[T]], It[T]]) -> It[T]:
        for callback in self._callbacks:
            self._iterator = callback(self._iterator)
        return fun(self._iterator)

    def consume(self, fun: t.Callable[[[T]], It[T]]):
        for callback in self._callbacks:
            self._iterator = callback(self._iterator)
        for it in self._iterator:
            fun(it)
        return

    def copy(self):
        return copy.deepcopy(self)

    def _to_iterator(self, iterable: t.Iterable[T]):
        for data in iterable:
            yield data
