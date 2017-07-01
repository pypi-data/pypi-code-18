from __future__ import absolute_import, unicode_literals

from wagtail.wagtailadmin.edit_handlers import FieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from django.db import models


# ########################################################
# Base classes
# ########################################################

class TestModel(models.Model):
    """A base class that all other 'menu' classes should inherit from."""
    name = models.CharField(max_length=255)
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('image'),
    ]
