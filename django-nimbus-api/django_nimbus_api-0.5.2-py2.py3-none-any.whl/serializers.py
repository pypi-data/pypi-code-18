# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.contrib.auth.models import User, Group
from django.utils import six
from rest_framework import serializers
from rest_framework.serializers import SerializerMetaclass


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups',)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class Serializer(serializers.Serializer):
    pass


class ListSerializer(serializers.ListSerializer):
    pass


class ModelSerializer(serializers.ModelSerializer):
    pass


class HyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    pass
