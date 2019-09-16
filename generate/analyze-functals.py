import numpy as np
import sys  # noqa
from PIL import Image
from utils import rgb2hsl
import operator

img = Image.open("../functals/functal-20171128153453133.jpg")

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
