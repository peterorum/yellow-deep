#!/usr/local/bin/python3

# finds the maximum value in the vector resulting from a matrix multiplcation

import tensorflow as tf
import numpy as np

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

x_data = np.random.randn(5, 10)
w_data = np.random.randn(10, 1)

x = tf.placeholder(tf.float32, shape=(5, 10))
w = tf.placeholder(tf.float32, shape=(10, 1))
b = tf.fill((5, 1), -1.)
xw = tf.matmul(x, w)

xwb = xw + b

s = tf.reduce_max(xwb)

with tf.Session() as sess:
    outs = sess.run(s, feed_dict={x: x_data, w: w_data})

print("outs = {}".format(outs))
