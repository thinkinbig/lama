import logging
import os
import unittest
import pandas as pd
from data import DATA_DIR
from lama.preprocessing.DataProcessor import change_object_col, reformat_dataframe, stream_groupby_csv
from lama.util.decorators import enable_logging


class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        self.list = pd.DataFrame(
            data={'col1': ['A', 'B', 'C', 'D', 'A'], 'col2': ['B', 'B', 'C', 'C', 'A']})

    def test_change_object_col(self):
        expected = [0, 1, 2, 3, 0]
        res = change_object_col(self.list['col1'])
        self.assertListEqual(expected, list(res))

    def test_reformat_dataframe(self):
        expected_col1 = [0, 1, 2, 3, 0]
        expected_col2 = [1, 1, 2, 2, 0]
        res = reformat_dataframe(
            self.list, ['col1', 'col2'], change_object_col)
        self.assertListEqual(expected_col1, list(res['col1']))
        self.assertListEqual(expected_col2, list(res['col2']))

    @enable_logging("test_stream_groupby_csv.log")
    def test_stream_groupby_csv(self):
        path = os.path.join(DATA_DIR, 'new_merchant_transactions.csv')
        key = 'card_id'
        for chunk in stream_groupby_csv(path, key):
            logger = logging.getLogger()
            logger.debug(chunk)


if __name__ == '__main__':
    unittest.main()
