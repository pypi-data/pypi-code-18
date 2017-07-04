# coding: utf-8


def iintersects(geometry_a, geometry_b):

    """Test to make sure that the geometry
    does not cover each other"""

    return geometry_a.intersects(geometry_b) and not geometry_a.touches(geometry_b)
