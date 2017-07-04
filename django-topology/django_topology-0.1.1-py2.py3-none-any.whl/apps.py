# -*- coding: utf-8
from django.apps import AppConfig


class TopologyConfig(AppConfig):
    name = 'topology'
    from topology.io import (
        to_multi,
        to_2d,
    )
    from topology.extensions import (
        iintersects,
    )
    from django.contrib.gis.geos import (
        GEOSGeometry,
    )
    GEOSGeometry.to_multi = to_multi
    GEOSGeometry.to_2d = to_2d
    GEOSGeometry.iintersects = iintersects
