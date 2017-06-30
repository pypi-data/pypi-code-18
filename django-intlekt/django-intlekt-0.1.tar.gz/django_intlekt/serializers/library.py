from rest_framework_mongoengine import serializers as mongoserializers
from rest_framework import serializers

from . import utils
from .. import models


def validate_translations_dict(translations):
    for lang in translations:
        utils.validate_language(lang)


def validate_text_dependencies_number(dependencies):
    # If there is one dependency only, the objects are considered equal.
    # For instance, a text with one word is the word itself.
    if len(dependencies) < 2:
        raise serializers.ValidationError('Must have two dependencies or more.')


def validate_text_dependencies_non_recursivity(dependencies):
    # A text cannot depend on another text. To include a text into another,
    # just copy all its dependencies.
    ids = [dep.id for dep in dependencies]
    usls = models.Text.objects(id__in=ids)
    if usls:
        raise serializers.ValidationError(
            'A text cannot contain another text. '
            'Instead, copy all its dependencies.'
        )


def serializer_factory(name, Model, extra_kwargs=None):
    extra_kwargs_ = extra_kwargs or {}

    class Meta:
        model = Model
        exclude = ('_cls',)
        extra_kwargs = {
            'translations': {'validators': [validate_translations_dict]},
            **extra_kwargs_,
        }

    return type(name, (mongoserializers.DocumentSerializer,), {'Meta': Meta})


class USLSerializer(mongoserializers.DocumentSerializer):
    class Meta:
        model = models.USL
        fields = '__all__'


TextSerializer = serializer_factory(
    'TextSerializer',
    models.Text,
    extra_kwargs={
        'dependencies': {
            'validators': [
                utils.validate_set,
                validate_text_dependencies_number,
                validate_text_dependencies_non_recursivity,
            ]
        }
    }
)

WordSerializer = serializer_factory('WordSerializer', models.Word)
