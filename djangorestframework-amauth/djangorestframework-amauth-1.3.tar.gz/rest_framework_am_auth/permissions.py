# -*- coding: utf-8 -*-
from rest_framework.permissions import DjangoModelPermissions, SAFE_METHODS


class AMPermissions(DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        # Workaround to ensure DjangoModelPermissions are not applied
        # to the root view when using DefaultRouter.
        if getattr(view, '_ignore_model_permissions', False):
            return True

        if hasattr(view, 'get_queryset'):
            queryset = view.get_queryset()
        else:
            queryset = getattr(view, 'queryset', None)

        assert queryset is not None, (
            'Cannot apply DjangoModelPermissions on a view that '
            'does not set `.queryset` or have a `.get_queryset()` method.'
        )

        perms = self.get_required_permissions(request.method, queryset.model)

        return (
            request.user and
            (request.auth or not self.authenticated_users_only) and
            request.auth.user_has_perms(perms)
        )
