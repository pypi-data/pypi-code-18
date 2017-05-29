from django.contrib.sites.models import Site
from django.db import models


class ResourceType(models.Model):
    """ Basis for selecting the appropriate view function for a resource """
    name = models.CharField(max_length=20, unique=True)
    cache = models.BooleanField(default=True)
    cache_max_age_in_seconds = models.IntegerField(default=5)


class Resource(models.Model):
    """ Unique URL published on one or more sites """
    slug = models.SlugField(max_length=2000)
    type = models.ForeignKey(ResourceType)
    sites = models.ManyToManyField(Site, through='SiteResource')
    available_on = models.DateTimeField(blank=True, null=True)
    available_until = models.DateTimeField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)


class SiteResource(models.Model):
    """ Ensure slugs are unique per site ("through" model for Resource.sites above) """
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('site', 'resource')
