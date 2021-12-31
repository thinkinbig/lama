from __future__ import annotations

import typing as t
import pandas as pd
import seaborn as sns

from lama.util.StreamerBuilder import StreamerBuilder, to_dictionary


class DataProcessor:

    def __init__(self, dataframes: t.List[pd.DataFrame], lables: t.List[str]):
        """
        Process the dataframes of the same columns, the Labels are putted to
        distinguish differnt dataframes. They must be of the same length
        """

        if len(dataframes) != len(lables):
            raise Exception("lables length must be the same with dataframes")
        self._mapper: t.Dict[str, pd.DataFrame] = {lables[i]: dataframes[i] for i in range(len(lables))}

    def nans(self, labels: t.List[str]) -> t.List[pd.DataFrame[bool]]:
        """
        Get how many nans in each columns
        """
        return StreamerBuilder.build(labels) \
            .map(lambda label: (label, self._mapper[label].isnull().sum())) \
            .collect(to_dictionary)

    def unique_columns(self, labels: t.List[str]) -> t.List[pd.DataFrame[bool]]:
        """
        Check if each columns are unique
        """
        return StreamerBuilder.build(labels) \
            .map(lambda label: (label, self._mapper[label].nunique() == self._mapper[label].shape[0])) \
            .collect(to_dictionary)

    def describe(self, labels: t.List[str], columns: t.List[str] | str):
        return StreamerBuilder.build(labels) \
            .map(lambda label: (label, self._mapper[label][columns].describe())) \
            .collect(to_dictionary)
