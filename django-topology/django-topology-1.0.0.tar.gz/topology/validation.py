# coding: utf-8
import six
from django.contrib.contenttypes.models import ContentType
from .utils import build_iintersects_filter
from .signals import (
    pre_check,
    post_check,
)
from .models import (
    TopologyRule,
    TopologyError,
)


class TopologyChecker(object):

    """
    Checks topology errors for
    objects and entire models.

    Inherits the name of the
    TopologyChecker by QGIS ;)
    """

    def __init__(self, persist=True, **kwargs):

        self.persist = persist
        self.arguments = kwargs

    def get_rules(self, model, rules='__all__'):
        """
        Gets all topology rules that
        model is the validated feature
        (content_type_a)
        """
        try:
            content_type_a = ContentType.objects.get(
                app_label=model._meta.app_label,
                model=model._meta.model_name
            )
        except ContentType.DoesNotExist:
            return

        qs = TopologyRule.objects.filter(
            content_type_a=content_type_a
        )

        if isinstance(rules, six.string_types) and rules == '__all__':
            return qs
        else:
            return qs.filter(rule__name__in=rules)

    def clean_errors(self, queryset, rules):

        """
        Deletes all errors
        that refere to a set of specific rules
        and specific features
        """

        TopologyError.objects.filter(
            topology_rule__in=[rule.pk for rule in rules],
            object_id_a__in=queryset.values_list('id', flat=True)
        ).delete()

    @property
    def extra_args(self):
        return self.arguments

    def validate(self, queryset, rules='__all__'):
        """
        Validates all features in the query
        for a set of rules
        If rules = '__all__' it will validate
        all the rules for that specific model
        """

        errors = {}
        model = queryset.model
        rules = self.get_rules(model, rules)

        self.clean_errors(queryset, rules)

        pre_check.send_robust(
            sender=self,
            queryset=queryset,
            rules=rules
        )

        for rule in rules:
            for feature in queryset:

                if rule.rule.name not in errors:
                    errors[rule.rule.name] = list()

                errors[rule.rule.name].extend(rule.validate(feature, **self.extra_args))
        if self.persist:
            for error_type, error_list in errors.items():
                for e in error_list:
                    e.save()

        post_check.send_robust(
            self,
            queryset=queryset,
            rules=rules,
            errors=errors
        )

        return errors

    def validate_feature(self, feature, rules='__all__'):
        model = feature._meta.model
        return self.validate(
            queryset=model.objects.filter(pk=feature.pk),
            rules=rules
        )

    def validate_extent(self, model, geometry, rules='__all__', geom_field='geom'):
        qs_filter = build_iintersects_filter(geometry, geom_field)
        qs = model.objects.filter(**qs_filter)
        return self.validate(
            queryset=qs,
            rules=rules
        )

    def validate_all(self, model, rules='__all__'):
        return self.validate(
            queryset=model.objects.all(),
            rules=rules
        )
