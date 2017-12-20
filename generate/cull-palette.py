#!/usr/local/bin/python3

# reduce number of negative results

# import sys
import json
import numpy as np

import pprint
pp = pprint.PrettyPrinter(indent=4)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

dataFile = '../data/train-all-palettes.json'

data = json.load(open(dataFile))

np.random.shuffle(data)

liked = [p for p in data if 'selected' in p and p['selected']]
disliked = [p for p in data if 'selected' not in p or not p['selected']][0: len(liked)]

new_data = liked + disliked

np.random.shuffle(new_data)

print('liked {} disliked {} all {}'.format(len(liked), len(disliked), len(new_data)))

filename = '../data/train-palettes.json'

with open(filename, 'w') as outfile:
    json.dump(new_data, outfile)
    outfile.close()
