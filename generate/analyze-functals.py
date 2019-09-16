import numpy as np
import json
import uuid
import sys  # noqa
from PIL import Image
from utils import rgb2hsl
import operator

filename = 'functal-20171128160309946.jpg'

img = Image.open(f"../functals/{filename}")

# generated from functals
palettes = []

colors = img.getcolors(img.size[0] * img.size[1])

# convert to hsl

hsls = []

for color in colors:
    (r, g, b) = color[1]

    hsl = rgb2hsl((r, g, b))

    hsls.append(hsl)

# convert to bins & count

max_bins = 4
bins = max_bins - 1  # rounding

color_bins = dict()

for hsl in hsls:
    hsl_binned = tuple([int(np.round(np.round(x * bins) / bins * 100)) for x in hsl])
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

palettes.append(palette)

# new palettes to auto-classify
filename = '../data/functal-palettes.json'

with open(filename, 'w') as outfile:
    json.dump(palettes, outfile, indent=4)
