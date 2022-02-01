import unittest

import lama.util as util
from lama.util.StreamerBuilder import StreamerBuilder


class TestStreamerBuilder(unittest.TestCase):

    def setUp(self):
        start = iter([1, 2, 3])
        self.builder = StreamerBuilder.build(start)

    def test_to_list(self):
        expected = [1, 2, 3]
        assert self.builder._iterator is not None
        result = self.builder.collect(util.to_list)
        self.assertListEqual(result, expected)

    def test_map(self):
        def my_sum(x):
            return x + 1

        expected = [2, 3, 4]
        result = self.builder.map(my_sum).collect(util.to_list)
        self.assertListEqual(result, expected)

    def test_filter(self):
        expected = [3]
        result = self.builder.filter(lambda x: x > 2).collect(util.to_list)
        self.assertListEqual(result, expected)

    def test_map_filter(self):
        expected = [3, 4]
        result = self.builder.map(
            lambda x: x + 1).filter(lambda x: x > 2).collect(util.to_list)
        self.assertListEqual(result, expected)

    def test_consume(self):
        self.builder.consume(print)

    def test_async_map_collect(self):
        def my_sum(x):
            return x + 1
        expected = [2, 3, 4]
        result = self.builder.async_map(my_sum).async_collect(util.to_list)
        self.assertListEqual(result, expected)

    def test_async_map_consume(self):
        self.builder.async_map(
            lambda x: x ** 2).async_consume(print)


if __name__ == '__main__':
    unittest.main()
