from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class DecimalField(serializers.IntegerField):

    def __init__(self, decimals=2, *args, **kwargs):
        assert decimals >= 1, (
            'decimals must be greater than or equal to 1'
        )

        self.decimals = decimals
        return super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        if data:
            return data / (10. ** self.decimals)
        return data

    def to_representation(self, obj):
        try:
            value = int(round(obj * 10 ** self.decimals))
        except (TypeError, ValueError):
            raise serializers.ValidationError(_('Invalid value'))
        return value
