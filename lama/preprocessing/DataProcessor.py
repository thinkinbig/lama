import typing as t
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.core.common import SettingWithCopyWarning

from lama.util.decorators import suppress_warning

def nans(df: pd.DataFrame) -> int:
    return df.isnull().sum()


def change_object_cols(se: pd.DataFrame, rule=lambda value: range(len(value))) -> np.ndarray:
    value = se.unique().tolist()
    value.sort()
    return se.map(pd.Series(rule(value), index=value)).values


@suppress_warning(warning=SettingWithCopyWarning)
def reformat_dataframe(df: pd.DataFrame, features: t.List[str], mapper) -> pd.DataFrame:
    """
    reformat the dataframe column by column with mapper, the function will replace 
    the given feature columns by slice, as python doesn't support pointer.


    if you would like to define a mapper function with more parameters, you can either define a 
    function using lambda or use functools.partial or functools.partialmethod

    for example:
        to define a change-object_cols function with self implemented rule
        mapper = functools.partial(change_object_cols, rule=${your_rule})
    """
    for feature in features:
        se_mapper = mapper(df[feature])
        df.loc[:, feature] = se_mapper
    return df

