# coding: utf-8
from django.contrib.gis.db.models import Union
from .models import (
    TopologyError,
)
from .utils import (
    build_iintersects_filter,
    build_contains_filter,
)


def must_be_contained(rule, feature):

    """
    this rule makes sure
    that the feature is
    contained within the boundaries
    of features from the B model

    A must be contained in B
    """

    model = rule.content_type_b.model_class()
    geom_field_a = rule.geom_field_a
    geom_field_b = rule.geom_field_b

    containers = model.objects.contains_feature(feature, geom_field_b)

    if containers.count() <= 0:
        intersecting = model.objects.iintersects_feature(feature, geom_field_b).aggregate(Union(geom_field_b))
        unioned_field = '%s__union' % geom_field_b
        unioned_geom = intersecting.get(unioned_field)
        if unioned_geom:
            leftover = getattr(feature, geom_field_a).difference(unioned_geom)
        else:
            leftover = getattr(feature, geom_field_a)
        return [
            TopologyError(
                content_type_a=rule.content_type_a,
                object_id_a=feature.pk,
                topology_rule=rule,
                geom=leftover
            )
        ]

    return []


def must_not_overlap(rule, feature):
    """
    this rule determines that
    this feature should not overlap
    with any feature on it's own model
    A should not overlap other A
    """
    errors = list()
    model = rule.content_type_a.model_class()
    geom_field = rule.geom_field_a
    intersecting = model.objects.iintersects_feature(feature, geom_field)
    target_geometry = getattr(feature, geom_field)
    for i in intersecting:
        errors.append(
            TopologyError(
                content_type_a=rule.content_type_a,
                object_id_a=i.pk,
                topology_rule=rule,
                geom=target_geometry.intersection(getattr(i, geom_field))
            )
        )

    return errors


def must_not_overlap_with(rule, feature):
    """
    this rule determines that this
    feature should not overlap any
    feature of the content_type_b
    of the rule
    A should not overlap B
    """
    errors = list()
    model = rule.content_type_b.model_class()
    geom_field_a = rule.geom_field_a
    geom_field_b = rule.geom_field_b
    target_geometry = getattr(feature, geom_field_a)

    # null and empty geometries do not produce errors ;)
    if not target_geometry or target_geometry.empty:
        return []

    intersecting = model.objects.iintersects(target_geometry, geom_field_b)

    for i in intersecting:
        errors.append(
            TopologyError(
                content_type_a=rule.content_type_a,
                object_id_a=feature.pk,
                content_type_b=rule.content_type_b,
                object_id_b=i.pk,
                topology_rule=rule,
                geom=target_geometry.intersection(getattr(i, geom_field_b))
            )
        )

    return errors
