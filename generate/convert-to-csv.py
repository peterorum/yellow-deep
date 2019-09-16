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

    h_max_bins = 12
    h_bins = h_max_bins - 1  # rounding

    s_max_bins = 4
    s_bins = s_max_bins - 1  # rounding

    l_max_bins = 4
    l_bins = l_max_bins - 1  # rounding

    # load data
    palettes = [{'id': p['id'], 'colors': p['colors'], 'selected': p['selected'] if 'selected' in p else False} for p in data]

    # convert each full color into its binned string version
    # eg hsl 0.5, 0.5, 0.5 -> hsl-050-050-050, depending on the number of bins

    # each palette is an array of the strings

    color_bins = []

    for palette in palettes:
        hsl = [[c['h'], c['s'], c['l']] for c in palette['colors']]

        hsl = [[
            int(np.round(np.round(color[0] * h_bins) / h_bins * 100)),
            int(np.round(np.round(color[1] * s_bins) / s_bins * 100)),
            int(np.round(np.round(color[2] * l_bins) / l_bins * 100))
        ] for color in hsl]

        # black, white, gray all same

        if hsl[2] == 0 or hsl[2] == 100:
            hsl = (0, 0, hsl[2])

        if hsl[1] == 0:
            hsl = (0, 0, hsl[2])

        hsl = [f'hsl-{x[0]:03d}-{x[1]:03d}-{x[2]:03d}' for x in hsl]

        # intensity = L * S, where L os 0 at 0 & 1, but 1 at 0.5

        intensity = [c['s'] * (1.0 - 2.0 * np.abs(0.5 - c['l'])) for c in palette['colors']]

        h_std = np.std([c['h'] for c in palette['colors']])
        s_std = np.std([c['s'] for c in palette['colors']])
        l_std = np.std([c['l'] for c in palette['colors']])
        i_std = np.std(intensity)

        s_avg = np.average([c['s'] for c in palette['colors']])
        l_avg = np.average([c['l'] for c in palette['colors']])
        i_avg = np.average(intensity)

        s_min = np.min([c['s'] for c in palette['colors']])
        l_min = np.min([c['l'] for c in palette['colors']])
        i_min = np.min(intensity)

        s_max = np.max([c['s'] for c in palette['colors']])
        l_max = np.max([c['l'] for c in palette['colors']])
        i_max = np.max(intensity)

        color_bins.append({'id': palette['id'], 'hsl': hsl, 'selected': palette['selected'],
                           'h_std': h_std, 's_std': s_std, 'l_std': l_std, 'i_std': i_std,
                           's_avg': s_avg, 'l_avg': l_avg, 'i_avg': i_avg,
                           's_min': s_min, 'l_min': l_min, 'i_min': i_min,
                           's_max': s_max, 'l_max': l_max, 'i_max': i_max})

    # now count occurences of each possible combination

    # create array of all possible colors

    h_bin_codes = [np.int(np.round(100 * b / (h_max_bins - 1))) for b in range(h_max_bins)]
    s_bin_codes = [np.int(np.round(100 * b / (s_max_bins - 1))) for b in range(s_max_bins)]
    l_bin_codes = [np.int(np.round(100 * b / (l_max_bins - 1))) for b in range(l_max_bins)]

    all_colors = []

    for b1 in h_bin_codes:
        for b2 in s_bin_codes:
            for b3 in l_bin_codes:
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
        encoded_colors.append({'id': cb['id'], 'colors': dic, 'selected': cb['selected'],
                               'h_std': cb['h_std'], 's_std': cb['s_std'], 'l_std': cb['l_std'], 'i_std': cb['i_std'],
                               's_avg': cb['s_avg'], 'l_avg': cb['l_avg'], 'i_avg': cb['i_avg'],
                               's_min': cb['s_min'], 'l_min': cb['l_min'], 'i_min': cb['i_min'],
                               's_max': cb['s_max'], 'l_max': cb['l_max'], 'i_max': cb['i_max']})

    # dump counted version to csv, with all colours as header

    with open(csv_file, 'w') as outfile:
        outfile.write('id,selected,')
        outfile.writelines([','.join(all_colors)])
        outfile.write(',h_std,s_std,l_std,i_std,s_avg,l_avg,i_avg,s_min,l_min,i_min,s_max,l_max,i_max')
        outfile.write('\n')

        for e in encoded_colors:
            outfile.write(f"{e['id']},")
            outfile.write('1,' if e['selected'] else '0,')
            outfile.write(','.join(str(e['colors'][c]) for c in all_colors))
            outfile.write(f",{e['h_std']},{e['s_std']},{e['l_std']},{e['i_std']}")
            outfile.write(
                f",{e['s_avg']},{e['l_avg']},{e['i_avg']}")
            outfile.write(
                f",{e['s_min']},{e['l_min']},{e['i_min']},{e['s_max']},{e['l_max']},{e['i_max']}")
            outfile.write('\n')


# --------main


convert_to_csv('manually-selected-palettes')
convert_to_csv('test-palettes')
convert_to_csv('functal-palettes')
# convert_to_csv('rules-palettes')
# convert_to_csv('red-green-palettes')
