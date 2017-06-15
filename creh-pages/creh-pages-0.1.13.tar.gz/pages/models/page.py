# -*- coding: utf-8 -*-
import itertools

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.db import models

from imagekit.models import ProcessedImageField

from pages.utils import constants
from pages.utils.image import get_slider_sizes, upload_picture_to
from pages.utils.database import SEOMixin, AuditableMixin, ActivatedMixin, ActivatedQuerySet


class CustomQuerySet(ActivatedQuerySet):

    def get_queryset(self):
        return ActivatedQuerySet(self.model, using=self._db)


class Page(SEOMixin, AuditableMixin, ActivatedMixin):

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=230,
    )

    external_url = models.URLField(
        verbose_name='External URL',
        max_length=500,
        blank=True,
    )

    type = models.SmallIntegerField(
        default=1,
        choices=constants.PAGE_TYPES
    )

    #Temp

    picture_pc = ProcessedImageField(
        upload_to=upload_picture_to,
        processors=get_slider_sizes(constants.PAGE_SLIDER_PC_SIZES),
        format=constants.PAGE_SLIDER_FORMAT,
        options=constants.PAGE_SLIDER_OPTIONS,
    )

    picture_tablet = ProcessedImageField(
        upload_to=upload_picture_to,
        processors=get_slider_sizes(constants.PAGE_SLIDER_TABLET_SIZES),
        format=constants.PAGE_SLIDER_FORMAT,
        options=constants.PAGE_SLIDER_OPTIONS,
        null=True
    )

    picture_mobile = ProcessedImageField(
        upload_to=upload_picture_to,
        processors=get_slider_sizes(constants.PAGE_SLIDER_MOBILE_SIZES),
        format=constants.PAGE_SLIDER_FORMAT,
        options=constants.PAGE_SLIDER_OPTIONS,
        null=True
    )

    picture_share = ProcessedImageField(
        upload_to=upload_picture_to,
        processors=get_slider_sizes(constants.PAGE_SLIDER_SHARE_SIZES),
        format=constants.PAGE_SLIDER_FORMAT,
        options=constants.PAGE_SLIDER_OPTIONS,
        null=True
    )

    objects = CustomQuerySet.as_manager()

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'pages'


class PageSEO(AuditableMixin, ActivatedMixin):
    url = models.URLField()
    title = models.CharField(
        max_length=250
    )
    description = models.CharField(
        max_length=250
    )
    keywords = models.CharField(
        max_length=250
    )
    page_type = models.CharField(
        max_length=250
    )
    share_image = models.ImageField()
    canonical_url = models.URLField()

    class Meta:
        db_table = 'pages_seo'


class PageTimer(AuditableMixin, ActivatedMixin):
    identifier = models.URLField()
    title = models.CharField(
        max_length=250
    )
    expire_date = models.DateTimeField()

    class Meta:
        db_table = 'pages_timer'


class PageTag(SEOMixin, AuditableMixin, ActivatedMixin):
    page = models.ForeignKey('Page')

    title = models.CharField(
        max_length=200,
    )

    slug = models.SlugField(
        max_length=230,
    )



@receiver(pre_save, sender=Page)
def pre_save_page(sender, instance=None, **kwargs):
    if constants.PAGE_AUTOSLUG:
        instance.slug = orig = slugify(instance.title)

        for x in itertools.count(1):
            if not Page.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

    return instance


@receiver(pre_save, sender=PageTag)
def pre_save_page_tag(sender, instance=None, **kwargs):
    if constants.PAGE_AUTOSLUG:
        instance.slug = orig = slugify(instance.title)

        for x in itertools.count(1):
            if not Page.objects.filter(slug=instance.slug).exists():
                break
            instance.slug = '%s-%d' % (orig, x)

    return instance