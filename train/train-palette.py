#!/usr/local/bin/python3

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import RMSprop, SGD

import numpy as np
# repeat random numbers
np.random.seed(1)

# import sys
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 128

# classes: 0 or 1
num_classes = 2

epochs = 100

validation_split = 0.2

optimizer = RMSprop()

dataFile = '../data/train-palettes.json'

data = json.load(open(dataFile))

# create list of lists of the hsl data
# each item is an array of 27 numbers (9 x hsl)

inputs_count = 27

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

# pp.pprint(colors)

# for each palette, [1] if selected, [0] if not
classifications = [[(1.0 if p['selected'] else 0.0) if 'selected' in p else 0.0] for p in data]

# use first 80% for training
count = len(colors)
train_count = int(count * 0.9)
test_count = int(count * 0.1)

x_train = np.array(colors[0:train_count])
x_test = np.array(colors[train_count:])

y_train = np.array(classifications[0:train_count])
y_test = np.array(classifications[train_count:])

print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()

# model.add(Dense(512, activation='relu', input_shape=(inputs_count,)))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(num_classes, activation='softmax'))

# v1 baseline single-layer model. train 86% val 82% test 76%
# model.add(Dense(num_classes, activation='softmax', input_shape=(inputs_count,)))

# v2 add hidden layers/ train 88% val 81% test 74%
hidden = 128
dropout_keep_prob = 0.5
model.add(Dense(hidden, activation='relu', input_shape=(inputs_count,)))
model.add(Dropout(dropout_keep_prob))
model.add(Dense(hidden, activation='relu', input_shape=(inputs_count,)))
model.add(Dropout(dropout_keep_prob))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=validation_split)

score = model.evaluate(x_test, y_test, verbose=0)

# install h5py
model.save('../models/palette.h5')

print('Test loss:', score[0])
print('Test accuracy:', score[1])
