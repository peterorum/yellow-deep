#!/usr/local/bin/python3

# train using a simple linear regression.
# assumes results are the product of the inputs and a weight matrix

import tensorflow as tf
import sys
import json
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

NUM_STEPS = 1000
# batch sizes are usually 50-500
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
train_results = good[0:trainCount]

test_colors = colors[-trainCount:]
test_results = good[-trainCount:]

# inputs - None will be sample aize
x = tf.placeholder(tf.float32, [None, 27])
# expected results
y = tf.placeholder(tf.float32, [None, 1])

# weights
w = tf.Variable(tf.zeros([27, 1]), name='weights')

# predicted result
y_pred = tf.matmul(x, w)

# loss is mean squared error
loss = tf.reduce_mean(tf.square(y - y_pred))

# cross entropy (a measure of similarity between two distributions)
# is mainly for categorical data.
# loss = tf.nn.softmax_cross_entropy_with_logits(logits=y_pred, labels=y)
# cross_entropy = tf.reduce_mean(loss)

learning_rate = 0.5

optimizer = tf.train.GradientDescentOptimizer(learning_rate)
train = optimizer.minimize(loss)

correct_mask = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_mask, tf.float32))


with tf.Session() as sess:

    # init
    sess.run(tf.global_variables_initializer())

    # train
    for step in range(NUM_STEPS):
        # batch_xs, batch_ys = tf_colors.next_batch(MINIBATCH_SIZE)
        sess.run(train, feed_dict={x: train_colors, y: train_results})

        if step % 100 == 0:
            print(step, sess.run([w]))
            # wb_.append(sess.run([w]))

    # test
    ans = sess.run(accuracy, feed_dict={x: test_colors,
                                        y: test_results})

    print("Accuracy: {:.4}%".format(ans * 100))
