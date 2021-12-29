from __future__ import annotations
import typing as t
import abc

import numpy as np

from lama.util import decorators

T = t.TypeVar('T')
U = t.TypeVar('U')


class StreamerBuilder:

    def __init__(self, iterator: t.Iterable[T]):
        if not isinstance(iterator, t.Iterator):
            raise Exception("Streamer Builder must accept an Iterator")
        self._iterator = iterator
        self._callbacks = []

    @staticmethod
    def build(iterator: t.Iterable[T]) -> StreamerBuilder:
        return StreamerBuilder(iterator)

    def map(self, f: t.Callable[[T], U]) -> StreamerBuilder:
        """
        Maps every unit in Iterator with function

        """

        def _mapper(iterator: t.Iterator[T]):
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

    def _register_callback(self, callback: t.Callable[..., t.Iterable[T]]):
        self._callbacks.append(callback)

    def collect(self, fun: t.Callable[[t.Iterable[T]], t.Iterable[T]]) -> t.Iterable[T]:
        for callback in self._callbacks:
            self._iterator = callback(self._iterator)
        return fun(self._iterator)

    @staticmethod
    def to_list(iterator: t.Iterable[T]) -> t.List[T]:
        return list(iterator)

    @staticmethod
    def to_ndarray(iterator: t.Iterable[T]) -> np.ndarray[T]:
        return np.asarray(list(iterator))
