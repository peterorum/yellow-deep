import numpy as np

import json

import sys  # noqa
import pprint
pp = pprint.PrettyPrinter(indent=4)


def convert_to_csv(file):

    json_file = f'../data/{file}.json'
    csv_file = f'../data/{file}.csv'

    data = json.load(open(json_file))

    # convert each palette to a csv of which colors it contains

    # how many divisions to divde each hsl into

    max_bins = 10

    bins = max_bins - 1  # rounding

    # load data
    palettes = [{'id': p['id'], 'colors': p['colors'], 'selected': p['selected'] if 'selected' in p else False} for p in data]

    # convert each full color into its binned string version
    # eg hsl 0.5, 0.5, 0.5 -> hsl-050-050-050, depending on the number of bins

    # each palette is an array of the strings

    color_bins = []

    for palette in palettes:
        hsl = [[c['h'], c['s'], c['l']] for c in palette['colors']]

        hsl = [[int(np.round(np.round(x * bins) / bins * 100)) for x in color] for color in hsl]

        hsl = [f'hsl-{x[0]:03d}-{x[1]:03d}-{x[2]:03d}' for x in hsl]

        color_bins.append({'id': palette['id'], 'hsl': hsl, 'selected': palette['selected']})

    # now count occurences of each possible combination

    # create array of all possible colors

    bin_codes = [np.int(np.round(100 * b / (max_bins - 1))) for b in range(max_bins)]

    all_colors = []

    for b1 in bin_codes:
        for b2 in bin_codes:
            for b3 in bin_codes:
                c = f'hsl-{b1:03d}-{b2:03d}-{b3:03d}'
                all_colors.append(c)

    # convert palettes into a count of how many of each color bin it has

    encoded_colors = []

    for cb in color_bins:

        dic = {}

        # all possible colors

        for c in all_colors:
            dic[c] = 0

        # count them

        for c in cb['hsl']:
            dic[c] += 1

        # store counted version
        encoded_colors.append({'id': cb['id'], 'colors': dic, 'selected': cb['selected']})

    # dump counted version to csv, with all colours as header

    with open(csv_file, 'w') as outfile:
        outfile.write('id,selected,')
        outfile.writelines([','.join(all_colors), '\n'])

        for e in encoded_colors:
            outfile.write(f"{e['id']},")
            outfile.write('1,' if e['selected'] else '0,')
            outfile.write(','.join(str(e['colors'][c]) for c in all_colors))
            outfile.write('\n')


# --------main


convert_to_csv('manually-selected-palettes')
convert_to_csv('test-palettes')
convert_to_csv('rules-palettes')
convert_to_csv('red-green-palettes')
