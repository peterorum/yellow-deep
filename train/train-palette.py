#!/usr/local/bin/python3

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop

import numpy as np
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

epochs = 20

dataFile = '../data/train-palettes.json'

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

# pp.pprint(colors)

# for each palette, [1] if selected, [0] if not
classifications = [[(1.0 if p['selected'] else 0.0) if 'selected' in p else 0.0] for p in data]

# use first 80% for training
count = len(colors)
trainCount = int(count * 0.8)
# validation & test count
testCount = int(count * 0.1)

x_train = np.array(colors[0:trainCount])
x_validation = np.array(colors[-testCount * 2: -testCount])
x_test = np.array(colors[-testCount:])

y_train = np.array(classifications[0:trainCount])
y_validation = np.array(classifications[-testCount * 2: -testCount])
y_test = np.array(classifications[-testCount:])

# x_train = x_train.reshape(trainCount, 27)
# x_test = x_test.reshape(testCount, 27)
# x_train = x_train.astype('float32')
# x_test = x_test.astype('float32')

print(x_train.shape[0], 'train samples')
print(x_validation.shape[0], 'validation samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_validation = keras.utils.to_categorical(y_validation, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()
model.add(Dense(512, activation='relu', input_shape=(27,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=RMSprop(),
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_validation, y_validation))

score = model.evaluate(x_test, y_test, verbose=0)

# install h5py
model.save('../models/palette.h5')

print('Test loss:', score[0])
print('Test accuracy:', score[1])
