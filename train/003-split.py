# basic training
# score 0.527
# minimize score

import json
import sys  # noqa
import warnings
from time import time
from pprint import pprint  # noqa
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

pd.options.display.float_format = '{:.4f}'.format
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
np.set_printoptions(threshold=sys.maxsize)

warnings.filterwarnings(module='sklearn*', action='ignore', category=DeprecationWarning)

zipext = ''
train_file = 'manually-selected-palettes'
# test_file = 'test-palettes'
test_file = 'functal-palettes'

start_time = time()
last_time = time()


def timer():
    global last_time

    print(f'{((time() - last_time) / 60):.1f} mins\n')  # noqa

    last_time = time()


def evaluate(train, test, unique_id, target):

    print('evaluate')

    lgb_model = lgb.LGBMClassifier(nthread=4, n_jobs=-1, verbose=-1, metric='rmse', objective='binary')

    x_train, x_test, y_train, y_test = train_test_split(train.drop(
        [unique_id, target], axis=1), train[target], test_size=0.2, random_state=1)

    lgb_model.fit(x_train, y_train)

    train_predictions = lgb_model.predict(x_test)
    train_score = np.sqrt(mean_squared_error(train_predictions, y_test))

    test_predictions = lgb_model.predict(test[x_train.columns])

    timer()

    return test_predictions, train_score


# --------------------- run


def run():

    unique_id = 'id'
    target = 'selected'

    # load data

    train = pd.read_csv(f'../data/{train_file}.csv{zipext}', index_col=False)
    test = pd.read_csv(f'../data/{test_file}.csv{zipext}', index_col=False)
    test_json = json.load(open(f'../data/{test_file}.json'))

    # ----------

    test_predictions, train_score = evaluate(train, test, unique_id, target)

    print('score', train_score)

    test[target] = test_predictions

    # save predictions to csv
    test[['id', 'selected']].to_csv('../data/predictions.csv', index=False)

    # save predictions back to json
    # assumes same sequence

    for i in range(0, len(test_json)):
        test_json[i]['selected'] = False if test.iloc[i].selected == 0 else True

    with open(f'../data/predictions.json', 'w') as outfile:
        json.dump(test_json, outfile, indent=4)


# -------- main


run()

print(f'Finished {((time() - start_time) / 60):.1f} mins\a')
