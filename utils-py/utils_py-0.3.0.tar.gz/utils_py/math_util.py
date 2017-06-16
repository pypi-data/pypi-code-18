#!/usr/bin/python
# -*- coding: utf-8 -*-

# Authors: Y. Jia <ytjia.zju@gmail.com>


def almost_eq(a, b, threshold=0.000001):
    """
    比较两个小数是否几乎相等
    当两数差的绝对值小于threshold时认为其相等
    :param a:
    :param b:
    :param threshold:
    :return: True or False
    """
    if abs(a - b) < threshold:
        return True
    else:
        return False
