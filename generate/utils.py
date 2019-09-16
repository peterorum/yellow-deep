def rgb2hsl(rgb):

    # rgb are all 0..255

    r = rgb[0] / 255.0
    g = rgb[1] / 255.0
    b = rgb[2] / 255.0

    f_max = max(r, g, b)
    f_min = min(r, g, b)

    h = 0
    s = 0
    l = (f_max + f_min) / 2.0

    if f_max == f_min:
        s = 0.0
        h = 0.0
    else:
        if l < 0.5:
            s = (f_max - f_min) / (f_max + f_min)
        else:
            s = (f_max - f_min) / (2.0 - f_max - f_min)

        f_delta = f_max - f_min

        if (r == f_max):
            h = (g - b) / f_delta
        elif g == f_max:
            h = 2.0 + (b - r) / f_delta
        else:
            h = 4.0 + (r - g) / f_delta

        h = h / 6.0

        if h < 0.0:
            h += 1.0

    return (h, s, l)
