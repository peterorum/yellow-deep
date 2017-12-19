#!/usr/local/bin/python3

# predict results for new palette & save selections back to the json

import keras
from keras.models import load_model

import numpy as np
np.random.seed(1)

np.set_printoptions(threshold=np.nan, precision=1, suppress=True)

# import sys
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# load trained model
model = load_model('../models/palette.h5')

dataFile = '../data/new-palettes.json'

data = json.load(open(dataFile))

# create list of lists of the hsl data
# each item is an array of 27 numbers (9 x hsl)

palettes = [p['colors'] for p in data]
colors = []

for palette in palettes:
    # flatten 9x3 to 27x1
    hsl = []

    for c in palette:
        hsl.append(c['h'])
        hsl.append(c['s'])
        hsl.append(c['l'])

    colors.append(hsl)

x_data = np.array(colors)

# predict

prediction = model.predict(x_data)

# print(prediction)

prediction = prediction.tolist()

min_like = 0.2

liked = len([1 for x in prediction if x[1] > min_like])  # x[0]])

pp.pprint('predicted likes {:3.2f}%'.format(liked / len(data) * 100))

for i in range(0, len(data)):
    data[i]['selected'] = prediction[i][1] > min_like  # prediction[i][0]

with open(dataFile, 'w') as outfile:
    json.dump(data, outfile)
