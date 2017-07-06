from rest_framework import viewsets
from rest_framework import serializers

import rest_framework_extras

from navbuilder.models import Menu, MenuItem


class MenuRelatedMixin(serializers.Serializer):
    menuitems = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="menuitem-detail"
    )

    class Meta(object):
        fields = ("menuitems", )


class MenuItemRelatedMixin(serializers.Serializer):
    submenuitems = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="menuitem-detail"
    )

    class Meta(object):
        fields = ("submenuitems", )


class PropertiesMixin(serializers.Serializer):
    absolute_url = serializers.ReadOnlyField()

    class Meta(object):
        fields = ("absolute_url", )


class MenuSerializer(MenuRelatedMixin, serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Menu


class MenuObjectsViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuItemSerializer(
        MenuItemRelatedMixin, PropertiesMixin,
        serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = MenuItem


class MenuItemObjectsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


def register(router):
    return rest_framework_extras.register(
        router, (
            ("navbuilder-menu", MenuObjectsViewSet),
            ("navbuilder-menuitem", MenuItemObjectsViewSet),
        )
    )
