from __future__ import annotations
import asyncio

from lama.util.decorators import suppress
from io import IOBase
import typing as t
import copy


T = t.TypeVar('T')
U = t.TypeVar('U')
V = t.TypeVar('V')
It = t.TypeVar('It', bound=t.Iterator)


class StreamerBuilder(t.Generic[T]):
    """

    StreamerBuilder is a wrapper class to wrap iterator and
    support chaining functions to make code more readable.

    The philosophy is that the functions won't
    be actually invoked until it is collected or consumed.

    This class is designed for io streams like TextFileReaders, but it also
    support normal iterators like list or array.

    While using normal iterator, remember that the builder is one-off.
    Since the streams will be lost after invoked.

    !!! Don't call it after collected or consumed !!!

    Args:
        t (generic type): Changed in runtime, no type inference engineering
    """

    def __init__(self, iterator: It[T]):
        if not isinstance(iterator, t.Iterable):
            raise Exception(
                "Streamer Builder must accept an instance from Iterable")
        self._iterator = iterator
        self._callbacks = []

    def __del__(self):
        # finalize stream
        if isinstance(self._iterator, IOBase) and not self._iterator.closed:
            self._iterator.close()
        del self._iterator

    @staticmethod
    def build(iterator: It[T]) -> StreamerBuilder:
        return StreamerBuilder(iterator)

    def map(self, function: t.Callable[[T], U]) -> StreamerBuilder:
        """
        Maps every unit in Iterator with function

        """

        def _mapper(iterator: It[T]) -> It[U]:
            for data in iterator:
                yield function(data)

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
        _iterator = self._iterator
        for callback in self._callbacks:
            _iterator = callback(_iterator)
        return fun(_iterator)

    def consume(self, fun: t.Callable[[T]]):
        _iterator = self._iterator
        for callback in self._callbacks:
            _iterator = callback(_iterator)
        for it in _iterator:
            fun(it)
        del self

    def copy(self):
        return copy.deepcopy(self)

    def async_map(self, mapper):
        self._callbacks.append(asyncio.coroutine(mapper))
        return self

    def async_collect(self, func):
        result = asyncio.get_event_loop().run_until_complete(self._aysnc_gather_iterator())
        return func(result)

    def async_consume(self, func):
        result = asyncio.get_event_loop().run_until_complete(self._aysnc_gather_iterator())
        func(result)

    def _async_connect(self, data):
        next = yield from self._callbacks[0](data)
        for f in self._callbacks[1:]:
            next = yield from f(next)
        return next

    async def _aysnc_gather_iterator(self):
        return await asyncio.gather(*[self._async_connect(value)
                                    for value in self._iterator])

    def _to_iterator(self, iterable: t.Iterable[T]):
        for data in iterable:
            yield data
