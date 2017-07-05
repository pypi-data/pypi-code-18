# coding: utf-8
import django
from .utils import (
    build_iintersects_filter,
    build_contains_filter,
)
from django.contrib.gis.db.models.query import GeoQuerySet
if django.VERSION <= (1, 9):
    from django.contrib.gis.db.models import GeoManager
else:
    from django.db.models import Manager as GeoManager


class TopologyQuerySet(GeoQuerySet):

    def contains(self, geometry, geom_field='geom'):

        if not geometry:
            return self.none()

        qs_filter = build_contains_filter(geometry, geom_field)
        return self.filter(**qs_filter)

    def contains_feature(self, feature, geom_field='geom'):
        """
        returns all the rows that contains a feature
        """
        if not geom_field:
            raise ValueError('geom_field is mandatory')

        if not feature:
            return self.none()

        geometry = getattr(feature, geom_field)

        if not geometry:
            return self.none()

        qs_filter = self.contains(geometry, geom_field)
        return qs_filter

    def iintersects(self, geometry, geom_field='geom'):
        """
        returns all rows that iintersects a geometry
        """
        if not geometry:
            return self.none()

        if not geom_field:
            raise ValueError('geom_field is mandatory')
        qs_filter = build_iintersects_filter(geometry, geom_field)
        return self.filter(**qs_filter)

    def iintersects_feature(self, feature, geom_field='geom'):

        """
        returns all the rows that iintersects a feature (or model instance)
        """
        if not geom_field:
            raise ValueError('geom_field is mandatory')

        if not feature:
            return self.none()

        geometry = getattr(feature, geom_field)

        if not geometry:
            return self.none()

        qs_filter = self.iintersects(getattr(feature, geom_field))
        if feature.pk:
            qs_filter = qs_filter.exclude(pk=feature.pk)
        return qs_filter


class TopologyManager(GeoManager):

    def get_queryset(self):
        return TopologyQuerySet(self.model, using=self._db)

    def iintersects(self, geometry, geom_field='geom'):
        return self.get_queryset().iintersects(geometry, geom_field)

    def iintersects_feature(self, feature, geom_field='geom'):
        return self.get_queryset().iintersects_feature(feature, geom_field)

    def contains(self, geometry, geom_field='geom'):
        return self.get_queryset().contains(geometry, geom_field)

    def contains_feature(self, feature, geom_field='geom'):
        return self.get_queryset().contains_feature(feature, geom_field)