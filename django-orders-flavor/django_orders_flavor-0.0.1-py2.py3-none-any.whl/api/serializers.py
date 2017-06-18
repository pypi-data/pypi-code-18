from core_flavor.api import fields as core_fields
from core_flavor.api import serializers as core_serializers
from core_flavor.shortcuts import import_from_string

from countries_flavor import models as countries_models
from rest_framework import serializers

from .. import models
from .. import settings as orders_settings


class ItemSerializer(core_serializers.PolymorphicSerializer):
    id = serializers.UUIDField(source='id.hex', read_only=True)
    price = core_fields.DecimalField()

    class Meta:
        model = models.Item
        fields = (
            'id', 'name', 'description', 'price', 'image',
            'modified', 'created')

        child_serializers = [
            import_from_string(serializer)
            for serializer in orders_settings.ORDERS_ITEMS_SERIALIZERS
        ]


class BaseOrderSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='id.hex', read_only=True)
    amount = core_fields.DecimalField(read_only=True)
    currency = serializers.PrimaryKeyRelatedField(
        queryset=countries_models.Currency.objects.all(),
        required=True)

    class Meta:
        model = models.Order
        fields = (
            'id', 'items', 'amount', 'currency', 'status',
            'status_changed', 'created')

        read_only_fields = ('status', 'status_changed')


class ItemInOrderBaseSerializer(serializers.ModelSerializer):
    price = core_fields.DecimalField(read_only=True)


class ItemInOrderWriteOnlySerializer(ItemInOrderBaseSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=models.Item.objects.all(),
        required=True)

    class Meta:
        model = models.ItemInOrder
        fields = ('id', 'quantity', 'price', 'tax_rate', 'created')
        read_only_fields = ('tax_rate',)


class ItemInOrderReadOnlySerializer(ItemInOrderBaseSerializer):
    item = ItemSerializer()

    class Meta:
        model = models.ItemInOrder
        fields = ('item', 'quantity', 'price', 'tax_rate', 'created')


class OrderWriteOnlySerializer(BaseOrderSerializer):
    items = ItemInOrderWriteOnlySerializer(many=True, source='items_in_order')

    def create(self, validated_data):
        items = validated_data.pop('items_in_order')
        validated_data['amount'] = (
            sum([item['id'].amount for item in items])
        )

        order = super().create(validated_data)

        for validated_data in items:
            item = validated_data.pop('id')
            models.ItemInOrder.objects.create(
                order_id=order.id,
                item_id=item.id,
                price=item.price,
                tax_rate=item.tax_rate,
                **validated_data)

        return order


class OrderReadOnlySerializer(BaseOrderSerializer):
    items = ItemInOrderReadOnlySerializer(many=True, source='items_in_order')
