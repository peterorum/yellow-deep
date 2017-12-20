#!/usr/local/bin/python3

# generate a json file of random hsl palettes.
# each palette is 9 colours

import numpy as np
import json
import uuid

palettes = []

for _ in range(0, 1000):
    palette = {'id': str(uuid.uuid1()), 'colors': []}

    selected = np.random.random() < 0.5

    # red or green
    h = 0.0 if selected else 0.4

    noise = np.random.uniform(-0.2, 0.2)

    h += noise

    tile = np.random.randint(0, 9)

    for p in range(0, 9):

        palette['colors'].append({
            'id': str(uuid.uuid1()),
            'h': h,
            's': np.random.uniform(0, 1),
            'l': np.random.uniform(0, 1)
        })

    palette['selected'] = selected

    palettes.append(palette)

# new palettes to auto-classify
filename = '../data/train-palettes.json'

with open(filename, 'w') as outfile:
    json.dump(palettes, outfile)
