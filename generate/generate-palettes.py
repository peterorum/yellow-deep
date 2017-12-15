#!/usr/local/bin/python3

# generate a json file of random hsl palettes.
# each palette is 9 colours

import numpy as np
import json
import uuid

palettes = []

for _ in range(0, 1000):
    palette = {'id': str(uuid.uuid1()), 'colors': []}

    for p in range(0, 9):
        palette['colors'].append({
            'id': str(uuid.uuid1()),
            'h': np.random.uniform(0, 1),
            's': np.random.uniform(0, 1),
            'l': np.random.uniform(0, 1)
        })

    palettes.append(palette)

# print(palettes)

with open('../data/train-palettes.json', 'w') as outfile:
    json.dump(palettes, outfile)
