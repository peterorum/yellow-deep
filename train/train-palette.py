#!/usr/local/bin/python3

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers.convolutional import Conv2D
from keras.optimizers import RMSprop
# from keras import regularizers
from keras.callbacks import TensorBoard

import numpy as np
# repeat random numbers
np.random.seed(1)

import sys
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 256

# classes: 0 or 1
num_classes = 2

epochs = 100

validation_split = 0.2

optimizer = RMSprop()

hidden = 256

dropout_keep_prob = 0.5

dataFile = '../data/train-palettes.json'

data = json.load(open(dataFile))

# create list of lists of the hsl data
# each item is an array of 27 numbers (9 x hsl)

inputs_count = 9

palettes = [p['colors'] for p in data]
colors = []

for palette in palettes:
    # 9x3
    hsl = [[c['h'], c['s'], c['l']] for c in palette]

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

callbacks = []
# tensorboard --logdir=../logs
callbacks.append(TensorBoard(log_dir='../logs', histogram_freq=0, write_graph=True, write_images=True))

model = Sequential()

# model.add(Dense(512, activation='relu', input_shape=(inputs_count,)))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(512, activation='relu'))
# model.add(Dropout(0.2))
# model.add(Dense(num_classes, activation='softmax'))

# v1 baseline single-layer model. train 86% val 82% test 76%
# model.add(Dense(num_classes, activation='softmax', input_shape=(inputs_count, 3)))

# v2 add hidden layers/ train 92% val 82% test 77%
# model.add(Dense(hidden, activation='relu', input_shape=(inputs_count, 3)))
# model.add(Dropout(dropout_keep_prob))
# model.add(Dense(hidden, activation='relu', input_shape=(inputs_count, 3)))
# model.add(Dropout(dropout_keep_prob))
# model.add(Dense(num_classes, activation='softmax'))

# v3 convolution
model.add(Conv2D(num_classes, (1, 1), activation='softmax', input_shape=(inputs_count, 3)))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=validation_split,
                    callbacks=callbacks
                    )

score = model.evaluate(x_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

# save

# must install h5py
# save model & weights for reloading
model.save('../models/palette.h5')

# save readable architecture
with open('../models/palette.json', 'w') as outfile:
    outfile.write(model.to_json())
    outfile.close()
