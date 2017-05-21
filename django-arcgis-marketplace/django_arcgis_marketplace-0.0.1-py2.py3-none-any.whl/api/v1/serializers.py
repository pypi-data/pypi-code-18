from core_flavor.api import fields as core_fields
from core_flavor.api import serializers as core_serializers

from rest_framework import serializers

from ... import models


__all__ = ['AccountSerializer', 'ItemSerializer']


class AccountSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='id.hex', read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update(instance.data)
        return data

    class Meta:
        model = models.Account
        fields = ('id',)


class ItemAccountSerializer(AccountSerializer):

    class Meta:
        model = models.Account
        fields = (
            'id', 'username', 'first_name', 'last_name', 'thumbnail', 'region'
        )

    def build_field(self, field_name, info, model_class, nested_depth):
        return self.build_property_field(field_name, model_class)


class WebMapingAppSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.WebMapingApp
        fields = ('purpose', 'file', 'api')


class ItemSerializer(core_serializers.PolymorphicSerializer):
    id = serializers.UUIDField(source='id.hex', read_only=True)
    owner = ItemAccountSerializer(read_only=True)
    price = core_fields.DecimalField()

    class Meta:
        model = models.Item
        fields = (
            'id', 'owner', 'title', 'description', 'price',
            'modified', 'created'
        )

        child_serializers = (
            WebMapingAppSerializer,
        )
