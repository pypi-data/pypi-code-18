import datetime

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_control
from django.views.decorators.http import last_modified

from mississippi.conf import conf
from mississippi.models import Resource, SiteResource


def dispatch(request: HttpRequest, slug: str) -> HttpResponse:
    """ Locate resource type, resource, and dispatch to view function in provided map """
    query = Resource.objects.select_related()
    resource = get_object_or_404(query, Q(sites=request.site) | Q(sites=None), slug__iexact=slug)

    view_fn = conf.MISSISSIPPI_VIEW_MAP.get(resource.type.name)
    if view_fn is None:
        raise ImproperlyConfigured('MISSISSIPPI_VIEW_MAP missing entry for "%s"' % resource.type.name)

    if resource.type.cache:
        @cache_control(public=True, max_age=resource.type.cache_max_age_in_seconds)
        @last_modified(lambda _, inner_resource: inner_resource.last_modified)
        def cached_view_fn(inner_request, inner_resource):
            return view_fn(inner_request, inner_resource)

        return cached_view_fn(request, resource)
    else:
        return view_fn


@cache_control(public=True, max_age=conf.MISSISSIPPI_SITEMAP_MAX_AGE)
def sitemap(request: HttpRequest) -> HttpResponse:
    """ Generate sitemap.xml """
    now = datetime.datetime.now()
    resources = Resource.objects.select_related()
    resources = resources.filter(Q(available_until__gt=now) | Q(available_until=None),
                                 Q(sites=request.site) | Q(sites=None),
                                 available_on__lte=now)
    resources = resources.order_by('-available_on')
    resources = resources[:50000]  # max allowed in sitemap.xml

    return render(request, 'mississippi/sitemap.xml', {'resources': resources}, 'application/xml; charset=UTF-8')
