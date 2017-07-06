from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


TARGET_CHOICES = (
    ("blank", "_blank"), ("parent", "_parent"),
    ("top", "_top"), ("self", "_self")
)


class Menu(models.Model):
    title = models.CharField(
        max_length=256, help_text="A short descriptive title."
    )
    slug = models.SlugField(max_length=256, db_index=True)

    class Meta:
        ordering = ["title"]

    def __unicode__(self):
        return self.title


class MenuItem(models.Model):
    title = models.CharField(
        max_length=256, help_text="A short descriptive title."
    )
    slug = models.SlugField(max_length=256, db_index=True)
    position = models.PositiveIntegerField()
    menu = models.ForeignKey(
        Menu, related_name="menuitems", blank=True, null=True
    )
    parent = models.ForeignKey(
        "self", related_name="submenuitems", blank=True, null=True
    )
    target = models.CharField(
        max_length=256, choices=TARGET_CHOICES, blank=True, null=True
    )
    link_content_type = models.ForeignKey(ContentType, blank=False, null=True)
    link_object_id = models.PositiveIntegerField(blank=False, null=True)
    link = GenericForeignKey("link_content_type", "link_object_id")
    root_menu = models.ForeignKey(Menu, null=True, editable=False)

    class Meta:
        ordering = ["position"]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):

        # Set the root menu
        parent = self.parent
        while getattr(parent, "parent", None) is not None:
            if parent is self:
                raise RuntimeError("Circular dependency detected")
            parent = parent.parent
        if parent is not None:
            self.root_menu = parent.menu
        else:
            self.root_menu = self.menu

        super(MenuItem, self).save(*args, **kwargs)

        # Set root menu for descendants. This will trigger the required
        # recursion.
        for child in self.submenuitems.all():
            child.save()

    def absolute_url(self):
        return self.get_absolute_url()

    def get_absolute_url(self):
        return self.link.get_absolute_url()
