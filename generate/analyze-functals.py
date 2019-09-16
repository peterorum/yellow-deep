import numpy as np
import json
import uuid
import os
import sys  # noqa
from PIL import Image
from utils import rgb2hsl
import operator
from os import listdir
from os.path import isfile, join
from pprint import pprint  # noqa

is_ec2 = os.environ['HOME'] == '/home/ec2-user'

functal_path = '/data/functal-images' if is_ec2 else '../classify/functals'

files = [f for f in listdir(functal_path) if isfile(join(functal_path, f))]

count = 0

for filename in files[0:5]:
    count = count + 1

    print(count, filename)

    img = Image.open(f"{functal_path}/{filename}")

    colors = img.getcolors(img.size[0] * img.size[1])

    # convert to hsl

    hsls = []

    for color in colors:
        (r, g, b) = color[1]

        hsl = rgb2hsl((r, g, b))

        hsls.append(hsl)

    # convert to bins & count

    h_max_bins = 12
    h_bins = h_max_bins - 1  # rounding

    s_max_bins = 4
    s_bins = s_max_bins - 1  # rounding

    l_max_bins = 4
    l_bins = l_max_bins - 1  # rounding

    color_bins = dict()

    for hsl in hsls:
        hsl_binned = (
            int(np.round(np.round(hsl[0] * h_bins) / h_bins * 100)),
            int(np.round(np.round(hsl[1] * s_bins) / s_bins * 100)),
            int(np.round(np.round(hsl[2] * l_bins) / l_bins * 100)))

        # black, white, gray all same

        if hsl_binned[2] == 0 or hsl_binned[2] == 100:
            hsl_binned = (0, 0, hsl_binned[2])

        if hsl_binned[1] == 0:
            hsl_binned = (0, 0, hsl_binned[2])

        color_bins[hsl_binned] = color_bins.get(hsl_binned, 0) + 1

    # sort by count
    color_bins = sorted(color_bins.items(), key=operator.itemgetter(1), reverse=True)

    most_common = color_bins[0:9]

    # convert to palette

    palette = {'id': str(uuid.uuid1()), 'image': filename, 'colors': [], }

    for p in range(0, 9):
        palette['colors'].append({
            'id': str(uuid.uuid1()),
            'h': color_bins[p][0][0] / 100,
            's': color_bins[p][0][1] / 100,
            'l': color_bins[p][0][2] / 100
        })

    # new palettes to auto-classify
    json_filename = f'/data/hsl-json/hsl-{filename}.json' if is_ec2 else f'../data/hsl-json/hsl-{filename}.json'

    with open(json_filename, 'w') as outfile:
        json.dump(palette, outfile, indent=4)
