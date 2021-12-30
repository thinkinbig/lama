import unittest

from lama.util import decorators


class TestDecorator(unittest.TestCase):

    @decorators.debug
    def test_log(self):
        print("Hello World!")


if __name__ == '__main__':
    unittest.main()
