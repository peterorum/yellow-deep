#!/usr/local/bin/python3

# generate a jsin file of random hsl

import numpy as np
import json

hsls = []

for _ in range(0, 1000):
    hsls.append({
        'h': np.random.uniform(0, 1),
        's': np.random.uniform(0, 1),
        'l': np.random.uniform(0, 1)
    })

# print(hsls)

with open('./data/train-hsls.json', 'w') as outfile:
    json.dump(hsls, outfile)
