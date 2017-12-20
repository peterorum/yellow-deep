#!/usr/local/bin/python3

# generate a json file of random hsl palettes.
# each palette is 9 colours

import numpy as np
import json
import uuid


def color_is_ok(hue):
    # ok 0-0.18, 0.47-0.8, 0.9-1
    # not ok 0.18-0.47, 0.8-0.9

    return (hue >= 0 and hue < 0.18) or (hue >= 0.47 and hue < 0.8) or (hue >= 0.9)

palettes = []

size = 100000

for _ in range(0, size):
    palette = {'id': str(uuid.uuid1()), 'colors': []}

    selected = np.random.random() < 0.5

    ls = [np.random.uniform(0, 1) for l in range(0, 9)]

    max_s = 0
    min_s = 1
    max_l = 0
    min_l = 1

    # intensity = saturation * (1 - 2 * abs(0.5 - lightness))
    # colors are most intense when l = 0.5
    max_i = 0

    for p in range(0, 9):
        h = np.random.uniform(0, 1)

        while color_is_ok(h) != selected:
            h = np.random.uniform(0, 1)

        s = np.random.uniform(0, 1)
        l = np.random.uniform(0, 1)

        max_s = max(max_s, s)
        min_s = min(min_s, s)

        max_l = max(max_l, l)
        min_l = min(min_l, l)

        max_i = max(max_i, s * (1 - 2 * abs(0.5 - l)))

        palette['colors'].append({
            'id': str(uuid.uuid1()),
            'h': h,
            's': s,
            'l': l
        })

    s_selected = max_s > 0.8
    l_selected = max_l > 0.9
    i_selected = max_i > 0.85

    palette['selected'] = selected and l_selected  # and s_selected

    palettes.append(palette)

# get equal number of likes & dislikes
liked = [p for p in palettes if p['selected']]
disliked = [p for p in palettes if not p['selected']][0: len(liked)]

data = liked + disliked

np.random.shuffle(data)

# new palettes to auto-classify
filename = '../data/train-palettes.json'

with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=4)
