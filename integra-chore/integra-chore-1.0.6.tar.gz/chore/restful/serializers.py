from rest_framework import serializers
import collections
from django.core.exceptions import ObjectDoesNotExist


class ModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelSerializer, self).__init__(*args, **kwargs)

    def getAttr(self, instance, attr):
        """
        It is a normal python attribute retrieve
        Can also be useful for dicts 
        """
        if instance is None:
            # Break out early if we get `None` at any point in a nested lookup.
            return None
        try:
            if isinstance(instance, collections.Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
        except ObjectDoesNotExist:
            return None
        return instance


class GridSerializer(serializers.ModelSerializer):

    grid_index = serializers.SerializerMethodField('grid_index_val')
    
    def __init__(self, *args, **kwargs):
        super(GridSerializer, self).__init__(*args, **kwargs)

    def grid_index_val(self, obj):
        return obj['grid_index']

    def getAttr(self, instance, attr):
        """
        It is a normal python attribute retrieve
        Can also be useful for dicts 
        """
        
        if instance is None:
            # Break out early if we get `None` at any point in a nested lookup.
            return None
        try:
            if isinstance(instance, collections.Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
        except ObjectDoesNotExist:
            return None
        return instance
    

class NormalSerializer(serializers.ModelSerializer):
    
    def __init__(self, *args, **kwargs):
        super(NormalSerializer, self).__init__(*args, **kwargs)

    def getAttr(self, instance, attr):
        """
        It is a normal python attribute retrieve
        Can also be useful for dicts 
        """
        if instance is None:
            # Break out early if we get `None` at any point in a nested lookup.
            return None
        try:
            if isinstance(instance, collections.Mapping):
                instance = instance[attr]
            else:
                instance = getattr(instance, attr)
        except ObjectDoesNotExist:
            return None
        return instance


    