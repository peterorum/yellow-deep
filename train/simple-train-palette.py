#!/usr/local/bin/python3

import json
import pprint
import os
import sys

import keras
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten  # pylint : disable=W0611
from keras.optimizers import RMSprop
from keras.callbacks import TensorBoard

import matplotlib.pyplot as plt

import numpy as np

# repeat random numbers
np.random.seed(1)

pp = pprint.PrettyPrinter(indent=4)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

batch_size = 256

# classes: 0 or 1
num_classes = 2

epochs = 120

validation_split = 0.2

optimizer = RMSprop()

hidden = 256

data_file = '../data/train-palettes.json'

data = json.load(open(data_file))

# create list of lists of the hsl data
# each item is an array of 27 numbers (9 x hsl)

inputs_count = 9

# palettes are 3 rows x 3 cols x 3 hsl
rows = 1
cols = 9
channels = 3

palettes = [p['colors'] for p in data]
colors = []

for palette in palettes:
    # 9x3
    hsl = [[c['h'], c['s'], c['l']] for c in palette]

    # 3x3x3
    colors.append([hsl])

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

print(x_train.shape, 'train shape')
print(x_train.shape[0], 'train samples')
print(x_test.shape[0], 'test samples')

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

callbacks = []
callbacks.append(TensorBoard(log_dir='../logs', histogram_freq=0, write_graph=True, write_images=True))

model = Sequential()

# v1 baseline single-layer model. train 86% val 82% test 76%
model.add(Dense(num_classes, activation='softmax', input_shape=(rows, cols, channels)))
model.add(Dense(num_classes))
model.add(Activation('relu'))

model.summary()


model.compile(loss='categorical_crossentropy',
              optimizer=optimizer,
              metrics=['accuracy'])

history = model.fit(x_train,
                    y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_split=validation_split,
                    callbacks=callbacks
                    )  # pylint: disable=C0330
sys.exit()

score = model.evaluate(x_test, y_test, verbose=0)

# save

# must install h5py
# save model & weights for reloading
model.save('../models/palette.h5')

# save readable architecture
with open('../models/palette.json', 'w') as outfile:
    outfile.write(model.to_json())
    outfile.close()

print('Test loss:', score[0])
print('Test accuracy:', score[1])

# list all data in history
# print(history.history.keys())

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.show()
