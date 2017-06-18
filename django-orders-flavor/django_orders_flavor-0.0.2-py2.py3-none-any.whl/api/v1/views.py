from rest_framework import viewsets
from rest_framework import permissions as api_permissions

from ... import models

from .. import permissions
from .. import serializers


class OrderViewSet(viewsets.ModelViewSet):
    lookup_value_regex = '[0-9a-f]{32}'

    permission_classes = (
        api_permissions.IsAuthenticated,
        permissions.IsStaffList,
        permissions.IsStaffOrOwner)

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return serializers.OrderWriteOnlySerializer
        return serializers.OrderReadOnlySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
