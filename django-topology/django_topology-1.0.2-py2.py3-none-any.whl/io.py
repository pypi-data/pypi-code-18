# coding: utf-8
from django.contrib.gis.geos import (
    GEOSGeometry,
    MultiPolygon,
    MultiLineString,
    MultiPoint
)
from django.contrib.gis.geos.prototypes.io import wkt_w


def to_pseudo(geometry):

    return geometry.transform(900913, clone=True)


def to_multi(geometry):

    """converts a geometry
    to a multi geometry"""

    if geometry.geom_type == 'Polygon':
        return MultiPolygon(geometry.clone(), srid=geometry.srid)

    if geometry.geom_type == 'LineString':
        return MultiLineString(geometry.clone(), srid=geometry.srid)

    if geometry.geom_type == 'Point':
        return MultiPoint(geometry.clone(), srid=geometry.srid)

    return geometry.clone()


def to_2d(geometry):

    """coerces a geometry to 2d"""

    if geometry.hasz:
        wkt = wkt_w(dim=2).write(geometry).decode()
        return GEOSGeometry(wkt, srid=geometry.srid)
    return geometry.clone()
