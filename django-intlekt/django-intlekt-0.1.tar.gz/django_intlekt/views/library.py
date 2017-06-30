from rest_framework import mixins
from rest_framework_mongoengine.viewsets import GenericViewSet as MEGenericViewSet
from rest_framework_mongoengine import viewsets as mongoviewsets

from . import utils
from .. import models
from .. import serializers


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


class WordViewSet(mongoviewsets.ModelViewSet):
    queryset = models.Word.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.WordSerializer

    @classmethod
    def get_view_description(cls, html=False):
        return utils.get_modelview_description(models.Word, html=html)

    def get_queryset(self):
        return models.Word.objects.all()


class TextViewSet(mongoviewsets.ModelViewSet):
    queryset = models.Text.objects.all()
    lookup_field = 'id'
    serializer_class = serializers.TextSerializer

    @classmethod
    def get_view_description(cls, html=False):
        return utils.get_modelview_description(models.Text, html=html)

    def get_queryset(self):
        return models.Text.objects.all()
