#!/usr/local/bin/python3

import tensorflow as tf
import sys
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

NUM_STEPS = 1000
MINIBATCH_SIZE = 100

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
good = [[(1.0 if p['selected'] else 0.0) if 'selected' in p else 0.0] for p in data]
# pp.pprint(good)

# use first 80% for training
count = len(colors)
trainCount = int(count * 0.8)

train_colors = colors[0:trainCount]
train_good = good[0:trainCount]

test_colors = colors[-trainCount:]
test_good = good[-trainCount:]


x = tf.placeholder(tf.float32, [None, 27])
W = tf.Variable(tf.zeros([27, 1]))

y_true = tf.placeholder(tf.float32, [None, 1])
y_pred = tf.matmul(x, W)

cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
    logits=y_pred, labels=y_true))


gd_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

correct_mask = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_true, 1))
accuracy = tf.reduce_mean(tf.cast(correct_mask, tf.float32))

with tf.Session() as sess:

    # train
    sess.run(tf.global_variables_initializer())

    for _ in range(NUM_STEPS):
        # batch_xs, batch_ys = tf_colors.next_batch(MINIBATCH_SIZE)
        sess.run(gd_step, feed_dict={x: train_colors, y_true: train_good})

    # test
    ans = sess.run(accuracy, feed_dict={x: test_colors,
                                        y_true: test_good})

    print("Accuracy: {:.4}%".format(ans * 100))
