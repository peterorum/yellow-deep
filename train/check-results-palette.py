#!/usr/local/bin/python3

# check actual results of training set

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

# classes: 0 or 1
num_classes = 2

dataFile = '../data/train-palettes.json'

data = json.load(open(dataFile))

# create list of lists of the hsl data
# each item is an array of 27 numbers (9 x hsl)

trainCount = int(len(data) * 0.8)

data = data[0:trainCount]

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

prediction = model.predict(x_data)

print(prediction)

correct = len([1 for x in prediction.tolist() if x[1] > x[0]])

actualCorrect = len([1 for x in data if 'selected' in x and x['selected']])

pp.pprint('actual correct {:3.2f}%'.format(actualCorrect / trainCount * 100))
pp.pprint('trained correct {:3.2f}%'.format(correct / trainCount * 100))
