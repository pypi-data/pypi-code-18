# coding: utf-8


def get_central_meridian(point):

    return (6 * int(point.x / 6)) + 3


def get_utm_zone(central_meridian):

    return 30 - abs(int(central_meridian / 6))
