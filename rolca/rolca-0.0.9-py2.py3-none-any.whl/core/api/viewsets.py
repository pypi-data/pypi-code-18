""".. Ignore pydocstyle D400.

=================
Core API viewsets
=================

.. autoclass:: rolca.core.api.viewsets.PhotoViewSet
    :members:

.. autoclass:: rolca.core.api.viewsets.ContestViewSet
    :members:

"""
import logging
from datetime import date

from django.db.models import Q

from rest_framework import viewsets

from rolca.core.api.permissions import AdminOrReadOnly
from rolca.core.api.serializers import ContestSerializer, PhotoSerializer
from rolca.core.models import Contest, Photo

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class PhotoViewSet(viewsets.ModelViewSet):
    """API view Photo objects."""

    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()

    def get_queryset(self):
        """Return queryset for photos that can be shown to user.

        Return:
        * all photos for already finished contests
        * user's photos
        """
        return Photo.objects.filter(
            Q(author__user=self.request.user) |
            Q(theme__contest__publish_date__lte=date.today()))


class ContestViewSet(viewsets.ModelViewSet):
    """API view Contest objects."""

    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = (AdminOrReadOnly,)
