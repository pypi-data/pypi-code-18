""".. Ignore pydocstyle D400.

====================
Core API serializers
====================

.. autoclass:: rolca.core.api.serializers.FileSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.PhotoSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.ThemeSerializer
    :members:

.. autoclass:: rolca.core.api.serializers.ContestSerializer
    :members:

"""
from rest_framework import serializers

from rolca.core.models import Contest, File, Photo, Theme


class FileSerializer(serializers.ModelSerializer):
    """Serializer for File objects."""

    class Meta:
        """Serializer configuration."""

        model = File
        fields = ('id', 'file',)


class PhotoSerializer(serializers.ModelSerializer):
    """Serializer for Photo objects."""

    photo = FileSerializer()

    class Meta:
        """Serializer configuration."""

        model = Photo
        fields = ('id', 'photo', 'title')


class ThemeSerializer(serializers.ModelSerializer):
    """Serializer for Theme objects."""

    class Meta:
        """Serializer configuration."""

        model = Theme
        fields = ('id', 'title', 'n_photos')


class ContestSerializer(serializers.ModelSerializer):
    """Serializer for Contest objects."""

    themes = ThemeSerializer(many=True, read_only=True)

    class Meta:
        """Serializer configuration."""

        model = Contest
        fields = ('id', 'title', 'start_date', 'end_date', 'themes')
