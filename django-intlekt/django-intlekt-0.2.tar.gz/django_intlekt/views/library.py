from rest_framework import mixins
from rest_framework_mongoengine.viewsets import GenericViewSet as MEGenericViewSet
from rest_framework_mongoengine import viewsets as mongoviewsets

from . import utils
from .. import models
from .. import serializers


def viewset_factory(model_name, lookup_field='id'):
    name = model_name + 'ViewSet'
    serializer_class = serializers.__dict__[model_name + 'Serializer']
    model = models.__dict__[model_name]

    def get_queryset(self):
        return model.objects.all()

    def get_view_description(cls, html=False):
        return utils.get_modelview_description(model, html=html)

    return type(
        name,
        (mongoviewsets.ModelViewSet,),
        {
            'queryset': model.objects.all(),
            'lookup_field': lookup_field,
            'serializer_class': serializer_class,
            'get_queryset': get_queryset,
            'get_view_description': classmethod(get_view_description),
        }
    )


GlossaryViewSet = viewset_factory('Glossary')
LexiconViewSet = viewset_factory('Lexicon')
WordViewSet = viewset_factory('Word')
TextViewSet = viewset_factory('Text')


class USLViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 MEGenericViewSet):
    queryset = models.USL.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.USLSerializer

    @classmethod
    def get_view_description(cls, html=False):
        return utils.get_modelview_description(models.USL, html=html)

    def get_queryset(self):
        return models.USL.objects.all()
