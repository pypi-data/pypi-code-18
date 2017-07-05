# coding: utf-8
from rest_framework import serializers
from .models import (
    Rule,
    TopologyRule,
    TopologyError,
)


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = (
            'id',
            'name',
            'description',
            'message',
            'method'
        )


class TopologyRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TopologyRule
        fields = (
            'id',
            'content_type_a',
            'geom_field_a',
            'content_type_b',
            'geom_field_b',
            'rule',
            'tolerance',
            'raises_error',
            'level',
            'custom_message',
        )


class TopologyErrorSerializer(serializers.ModelSerializer):

    message = serializers.SerializerMethodField()

    def get_message(self, obj):
        return obj.__str__()

    class Meta:
        model = TopologyError
        fields = (
            'id',
            'content_type_a',
            'object_id_a',
            'content_type_b',
            'object_id_b',
            'topology_rule',
            'message',
            'geom',
        )
