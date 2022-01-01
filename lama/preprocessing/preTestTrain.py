import os
import gc

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from data import DATA_DIR
from lama.preprocessing.DataProcessor import nans, change_object_cols

OUT_DIR = os.path.join(DATA_DIR, "pre")

df_test = pd.read_csv(os.path.join(DATA_DIR, 'test.csv'), header=0)
df_train = pd.read_csv(os.path.join(DATA_DIR, 'train.csv'), header=0)

# check nans
print(nans(df_test))
print(nans(df_train))

# There is only one nan in test, so we simply throw it away
df_test_copy = df_test.dropna()
df_train_copy = df_train

del df_test
del df_train
gc.collect()

# check noise
sns.histplot(df_train_copy['target'], kde=True).set(title="HistPlot of Train Target")
plt.show()

# We can see the unexpected values in target < -30, We'll handle this later
unexpected = (df_train_copy['target'] < -30).sum()

# check unique id
train_count = df_train_copy.shape[0]
test_count = df_test_copy.shape[0]
print(df_train_copy['card_id'].nunique() == train_count)
print(df_test_copy['card_id'].nunique() == test_count)

# check if test and train are fairly distributed
features = ['first_active_month', 'feature_1', 'feature_2', 'feature_3']
for feature in features:
    (df_train_copy[feature].value_counts().sort_index() / train_count).plot()
    (df_test_copy[feature].value_counts().sort_index() / test_count).plot()
    plt.legend(['train', 'test'])
    plt.xlabel(feature)
    plt.ylabel('ratio')
    plt.show()

# There is no need to tune

# The last step is to convert all columns type of object to int
print(df_test_copy.info())
# convert first_active_month to int
se_mapper = change_object_cols(df_train_copy['first_active_month'].append(df_test_copy['first_active_month']))
df_train_copy['first_active_month'] = se_mapper[:train_count]
df_test_copy['first_active_month'] = se_mapper[train_count:]


df_test_copy.to_csv(os.path.join(OUT_DIR, 'test_pre.csv'), index=False)
df_train_copy.to_csv(os.path.join(OUT_DIR, 'train_pre.csv'), index=False)

