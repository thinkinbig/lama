import os

import pandas as pd

from data import DATA_DIR
from lama.preprocessing.DataProcessor import DataProcessor

df_test = pd.read_csv(os.path.join(DATA_DIR, 'test.csv'), header=0)
df_train = pd.read_csv(os.path.join(DATA_DIR, 'train.csv'), header=0)
processor = DataProcessor([df_train, df_test], ["train", "test"])

# not all features are filled
labels = ["train", "test"]
nans = processor.nans(labels)
uniques = processor.unique_columns(labels)


# check if train and test are identical
# check target in train
target = processor.describe(["train"], "target")


