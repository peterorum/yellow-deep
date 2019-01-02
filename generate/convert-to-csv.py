#!/usr/local/bin/python3

import numpy as np

import json

import sys
import pprint
pp = pprint.PrettyPrinter(indent=4)

data_file = '../data/manually-selected-palettes.json'

data = json.load(open(data_file))

# convert each palette to a csv of which colors it contains

# how many divisions to divde each hsl into

max_bins = 10

bins = max_bins - 1  # rounding

palettes = [p['colors'] for p in data]

color_bins = []

for palette in palettes:
    hsl = [[c['h'], c['s'], c['l']] for c in palette]

    hsl = [[int(np.round(np.round(x * bins) / bins * 100)) for x in color] for color in hsl]

    hsl = [f'hsl-{x[0]:03d}-{x[1]:03d}-{x[2]:03d}' for x in hsl]

    color_bins.append(hsl)

# now count occurences of each possible combination

bin_codes = [np.int(np.round(100 * b / (max_bins - 1))) for b in range(max_bins)]

all_colors = []

for b1 in bin_codes:
    for b2 in bin_codes:
        for b3 in bin_codes:
            c = f'hsl-{b1:03d}-{b2:03d}-{b3:03d}'
            all_colors.append(c)

encoded_colors = []

for cb in color_bins:

    dic = {}

    for c in all_colors:
        dic[c] = 0

    for c in cb:
        dic[c] += 1

    encoded_colors.append(dic)

csv_filename = '../data/manually-selected-palettes.csv'

with open(csv_filename, 'w') as outfile:
    outfile.writelines([','.join(all_colors), '\n'])

    for e in encoded_colors:
        outfile.write(','.join(str(e[c]) for c in all_colors))
        outfile.write('\n')
