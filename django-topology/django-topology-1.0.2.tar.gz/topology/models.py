# coding: utf-8
import importlib
from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .utils import validation_error_class
from .choices import LEVEL_CHOICES, LEVEL_CHOICES_WARNING


class Rule(models.Model):

    name = models.CharField(
        max_length=64,
        verbose_name=_('Name')
    )

    description = models.CharField(
        max_length=256,
        verbose_name=_('Description'),
        null=True
    )

    message = models.CharField(
        max_length=256,
        verbose_name=_('Message'),
    )

    method = models.CharField(
        max_length=256,
        verbose_name=_('Method'),
    )

    def get_method(self):
        try:
            parts = self.method.split('.')
            module = '.'.join(parts[:-1])
            method_name = parts[-1]
            module = importlib.import_module(module)
            return getattr(module, method_name, None)
        except Exception as ex:
            return None

    def __str__(self):

        return self.name

    class Meta:

        verbose_name = _('Rule')
        verbose_name_plural = _('Rules')


class TopologyRule(models.Model):

    """models a topology rule
    to be applied to a layer"""

    content_type_a = models.ForeignKey(
        ContentType,
        verbose_name=_('Model A'),
        related_name='topology_rules_a'
    )

    geom_field_a = models.CharField(
        max_length=128,
        verbose_name=_('Geometry Field A'),
        default='geom'
    )

    content_type_b = models.ForeignKey(
        ContentType,
        verbose_name=_('Model B'),
        related_name='topology_rules_b',
        null=True
    )

    geom_field_b = models.CharField(
        max_length=128,
        verbose_name=_('Geometry Field B'),
        null=True
    )

    rule = models.ForeignKey(
        Rule,
        verbose_name=_('Rule')
    )

    tolerance = models.FloatField(
        verbose_name=_('Tolerance'),
        null=True
    )

    raises_error = models.BooleanField(
        verbose_name=_('Raises Error?'),
        help_text=_('If this raises an error, the user will not be able to save a new or existing object, if it fails on validation.'),  # noqa,
        default=False
    )

    level = models.CharField(
        verbose_name=('Error Level'),
        max_length=32,
        choices=LEVEL_CHOICES,
        default=LEVEL_CHOICES_WARNING,
    )

    custom_message = models.CharField(
        verbose_name=_('Custom Message'),
        max_length=512,
        help_text=_('Supports interpolation for placeholders model_a, model_b and rule.'),
        null=True
    )

    def validate(self, feature, **kwargs):

        """Validates a feature"""

        validation_method = self.rule.get_method()
        errors = validation_method(self, feature, **kwargs)
        ValidationError = validation_error_class()
        if errors and self.raises_error:
            raise ValidationError(errors[0].message)
        return errors

    def __str__(self):
        if self.content_type_a and self.content_type_b:
            return _('%(model_a)s %(rule)s %(model_b)s') % {'model_a': self.content_type_a,
                                                            'rule': self.rule,
                                                            'model_b': self.content_type_b}
        else:
            return _('%(model_a)s %(rule)s') % {'model_a': self.content_type_a,
                                                'rule': self.rule}

    class Meta:

        verbose_name = _('Topology Rule')
        verbose_name_plural = _('Topology Rules')


class TopologyError(models.Model):

    content_type_a = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='errors_a'
    )

    object_id_a = models.PositiveIntegerField()

    object_a = GenericForeignKey('content_type_a', 'object_id_a')

    content_type_b = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name='errors_b',
        null=True
    )

    object_id_b = models.PositiveIntegerField(
        null=True
    )

    object_b = GenericForeignKey('content_type_b', 'object_id_b')

    topology_rule = models.ForeignKey(
        TopologyRule,
        verbose_name=_('Topology Rule')
    )

    geom = models.GeometryField(
        null=True
    )

    def __str__(self):
        if self.object_id_a and self.object_id_b:
            return _('%(model_a)s %(rule)s %(model_b)s') % {'model_a': self.object_id_a,
                                                            'rule': self.topology_rule.rule.message,
                                                            'model_b': self.object_id_b}
        else:
            return _('%(model_a)s %(rule)s') % {'model_a': self.object_id_a,
                                                'rule': self.topology_rule.rule.message}

    class Meta:

        verbose_name = _('Topology Error')
        verbose_name_plural = _('Topology Errors')
