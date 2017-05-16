# from __future__ import unicode_literals
from rest_framework import serializers
from rest_framework.reverse import reverse

from ....models import FormEntry

__title__ = 'fobi.contrib.apps.drf_integration.serializers'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FormEntrySerializer',)


class FormEntrySerializer(serializers.ModelSerializer):
    """FormEntry serializer (read-only).

    Used for detail and list views.
    """
    url = serializers.SerializerMethodField()

    class Meta(object):
        """Options."""

        model = FormEntry
        fields = (
            'url',
            'id',
            'slug',
            'title',
        )
        read_only_fields = (
            'url',
            'id',
            'slug',
            'title',
        )

    def get_url(self, obj):
        """Get URL."""
        return reverse(
            'fobi_form_entry-detail',
            args=[obj.slug],
            request=self.context['request']
        )
