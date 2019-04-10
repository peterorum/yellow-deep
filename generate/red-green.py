#!/usr/local/bin/python3

# generate a json file of random hsl palettes.
# each palette is 9 colours

import json
import uuid
import time
import datetime
import numpy as np


def color_is_ok(hue):
    # ok 0-0.18, 0.47-0.8, 0.9-1
    # not ok 0.18-0.47, 0.8-0.9

    return (hue >= 0 and hue < 0.18) or (hue >= 0.47 and hue < 0.8) or (hue >= 0.9)

# --- start


start_time = time.time()

palettes = []

likes_required = 5000

selected_count = 0

while selected_count < likes_required:
    palette = {'id': str(uuid.uuid1()), 'colors': []}

    has_unacceptable_color = False

    max_s = 0
    min_s = 1
    max_l = 0
    min_l = 1

    for p in range(0, 9):

        h = np.random.uniform(0, 1)
        s = np.random.uniform(0, 1)
        l = np.random.uniform(0, 1)

        has_unacceptable_color = has_unacceptable_color or not color_is_ok(h)

        max_s = max(max_s, s)
        min_s = min(min_s, s)

        max_l = max(max_l, l)
        min_l = min(min_l, l)

        palette['colors'].append({
            'id': str(uuid.uuid1()),
            'h': h,
            's': s,
            'l': l
        })

    h_selected = not has_unacceptable_color
    s_selected = True  # max_s > 0.8
    l_selected = min_l < 0.1 and max_l > 0.9

    selected = h_selected and s_selected and l_selected

    palette['selected'] = selected

    palettes.append(palette)

    if selected:
        selected_count += 1
        elapsed_time = time.time() - start_time
        print('\r{} eta {}'.format(selected_count, datetime.timedelta(
            seconds=np.round(elapsed_time / selected_count * (likes_required - selected_count)))), end='')

    if selected_count > likes_required:
        break

# get equal number of likes & dislikes
liked = [p for p in palettes if p['selected']]
disliked = [p for p in palettes if not p['selected']][0: len(liked)]

data = liked + disliked

np.random.shuffle(data)

# new palettes to auto-classify
filename = '../data/red-green-palettes.json'

with open(filename, 'w') as outfile:
    json.dump(data, outfile, indent=4)
