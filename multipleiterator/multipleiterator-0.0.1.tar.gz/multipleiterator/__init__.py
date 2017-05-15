# coding=utf8

import functools

def _combine_two (iter0, iter1):
    for it0 in iter0:
        for it1 in iter1:
            if isinstance(it0, list):
                yield it0 + [it1, ]
            else:
                yield [it0, it1]

def multipleiter(*iters):
    rs_arr = functools.reduce(_combine_two, iters)
    return rs_arr
