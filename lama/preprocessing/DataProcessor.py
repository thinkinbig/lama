import typing as t
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from pandas.core.common import SettingWithCopyWarning
from lama.util import to_list

from lama.util.decorators import suppress


def nans(df: pd.DataFrame) -> int:
    return df.isnull().sum()


def change_object_col(se: pd.DataFrame, rule=lambda value: range(len(value))) -> pd.DataFrame:
    """

    change object type to numerical type
    if the dataframe contains nan, which means the value will be processed later,the method will leave it intact.

    Args:
        se (pd.DataFrame): [dataframe to change]
        rule ([object], int): [rule to cahnge the column]. Defaults to lambdavalue:range(len(value)).

    Returns:
        np.ndarray: [df dataframe or numpy arrat]
    """

    se.fillna(-1, inplace=True)
    value = se.unique().tolist()
    if -1 in value:
        value.remove(-1)
        keys = to_list(rule(value))
        keys.insert(0, -1)
        value.sort()
        value.insert(0, -1)
    else:
        value.sort()
        keys = rule(value)
    return se.map(pd.Series(keys, index=value)).values


def standarize_col(df: pd.DataFrame) -> np.ndarray:
    return preprocessing.StandardScaler().fit_transform(df.values.reshape(-1, 1))


@suppress(excepts=SettingWithCopyWarning)
def reformat_dataframe(df: pd.DataFrame, features: t.List[str], mapper: t.Callable[[pd.DataFrame], pd.DataFrame]) -> pd.DataFrame:
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
        df[feature] = se_mapper
    return df


def split_with_index(df: pd.DataFrame, index: int) -> t.Iterable[pd.DataFrame]:
    yield df[:index]
    yield df[index:]


def stream_groupby_csv(path: str, key: str, chunk_size: int = 10**6, dtype=None) -> t.Iterable[pd.DataFrame]:
    """
    A stream provider that reads from large csv file
    and group the csv by key

    Args:
        path (str): filepath
        key (str): key to groupby
        chunk_size (int, optional): chunksize. Defaults to 10**6.
        dtype (DtypeLike, optional): Dtype. Defaults to None.
    """

    with pd.read_csv(path, chunksize=chunk_size, dtype=dtype) as reader:
        orphans = pd.DataFrame()
        for chunk in reader:
            # Add the previous orphans to the chunk
            chunk = pd.concat((orphans, chunk))

            last_val = chunk[key].iloc[-1]
            is_orphan = chunk[key] == last_val

            orphans = chunk[is_orphan]
            yield chunk[~is_orphan]

        if len(orphans):
            yield orphans
