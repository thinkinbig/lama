from __future__ import annotations
import typing as t

import numpy as np

T = t.TypeVar('T')
U = t.TypeVar('U')
V = t.TypeVar('V')
It = t.TypeVar('It', bound=t.Iterator)


def to_dictionary(iterator: It[T], key_mapper: t.Callable[[T], V] = lambda it: it[0],
                  values_mapper: t.Callable[[T], U] = lambda it: it[1]) -> t.Dict[V, U]:
    return {key_mapper(it): values_mapper(it) for it in iterator}


def to_list(iterator: It[T]) -> t.List[T]:
    return list(iterator)


def to_ndarray(iterator: It[T], dtpye) -> np.narray[T]:
    return np.asarray(list(iterator), dtpye)


class StreamerBuilder:

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

    def _register_callback(self, callback: t.Callable[..., t.Iterable[T]]):
        self._callbacks.append(callback)

    def collect(self, fun: t.Callable[[It[T]], It[T]]) -> It[T]:
        for callback in self._callbacks:
            self._iterator = callback(self._iterator)
        return fun(self._iterator)

