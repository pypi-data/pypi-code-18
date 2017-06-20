import numpy as np


def append(a, b, axis=0):
    a = pad(a, np.shape(b), axis=axis)
    b = pad(b, np.shape(a), axis=axis)
    return np.append(a, b, axis=axis)


def concatenate(xs, axis=0):
    shape = list(np.shape(xs[0]))
    for x in xs:
        for i, dim in enumerate(np.shape(x)):
            shape[i] = max(shape[i], dim)
    new_xs = [pad(x, shape, axis=axis) for x in xs]
    return np.concatenate(new_xs, axis=axis)


def pad(target, shape, axis=0):
    widths = []
    for i, (dt, ds) in enumerate(zip(np.shape(target), shape)):
        if i == axis:
            widths.append([0, 0])
        else:
            widths.append([0, max(0, ds-dt)])
    return np.pad(target, widths, 'constant')
