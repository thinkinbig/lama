import pandas as pd


def nans(df: pd.DataFrame):
    return df.isnull().sum()


def change_object_cols(se: pd.DataFrame):
    value = se.unique().tolist()
    value.sort()
    return se.map(pd.Series(range(len(value)), index=value)).values
