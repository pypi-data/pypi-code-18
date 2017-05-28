import datetime
from xml.etree import ElementTree

from django.conf import settings
from django.contrib.sites.models import Site
from django.http import HttpRequest, HttpResponse, Http404
from django.test import TestCase

from mississippi import models, views
from mississippi.models import Resource, ResourceType


class DispatchTestCase(TestCase):
    """ Ensure incoming requests and slugs get views.dispatched to correct view functions """

    def setUp(self):
        self.site1 = Site.objects.create(domain='site1.test.com')
        self.site2 = Site.objects.create(domain='site2.test.com')

        self.article_type = ResourceType.objects.create(name='article')
        self.event_type = ResourceType.objects.create(name='event')

        self.article_for_one_site = Resource.objects.create(slug='article1', type=self.article_type)
        models.SiteResource.objects.create(site=self.site1, resource=self.article_for_one_site)
        self.article_for_two_sites = Resource.objects.create(slug='article2', type=self.article_type)
        models.SiteResource.objects.create(site=self.site1, resource=self.article_for_two_sites)
        models.SiteResource.objects.create(site=self.site2, resource=self.article_for_two_sites)
        self.article_for_all_sites = Resource.objects.create(slug='article3', type=self.article_type)

    def dispatches_to_resource_with_one_site(self):
        # Set up
        actual_request = None
        actual_resource = None

        def view_fn(request, resource):
            nonlocal actual_request
            actual_request = request
            nonlocal actual_resource
            actual_resource = resource
            return HttpResponse()

        settings.MISSISSIPPI_VIEW_MAP = {
            'article': view_fn,
        }

        request = HttpRequest()
        request.site = self.site1

        # Run
        views.dispatch(request, self.article_for_one_site.slug)

        # Test
        self.assertEqual(request, actual_request)
        self.assertEqual(self.article_for_one_site, actual_resource)

    def test_dispatches_to_resource_with_multiple_sites(self):
        # Set up
        actual_request = None
        actual_resource = None

        def view_fn(request, resource):
            nonlocal actual_request
            actual_request = request
            nonlocal actual_resource
            actual_resource = resource
            return HttpResponse()

        settings.MISSISSIPPI_VIEW_MAP = {
            'article': view_fn,
        }

        request = HttpRequest()
        request.site = self.site1

        # Run
        views.dispatch(request, self.article_for_two_sites.slug)

        # Test
        self.assertEqual(request, actual_request)
        self.assertEqual(self.article_for_two_sites, actual_resource)

    def test_dispatches_to_resource_with_no_sites(self):
        # Set up
        actual_request = None
        actual_resource = None

        def view_fn(request, resource):
            nonlocal actual_request
            actual_request = request
            nonlocal actual_resource
            actual_resource = resource
            return HttpResponse()

        settings.MISSISSIPPI_VIEW_MAP = {
            'article': view_fn,
        }

        request = HttpRequest()
        request.site = self.site1

        # Run
        views.dispatch(request, self.article_for_all_sites.slug)

        # Test
        self.assertEqual(request, actual_request)
        self.assertEqual(self.article_for_all_sites, actual_resource)

    def test_throws_404_when_no_resource(self):
        # Set up
        request = HttpRequest()
        request.site = self.site1
        threw_404 = False

        # Run
        try:
            views.dispatch(request, 'nopenopenope')
        except Http404:
            return

        # Test
        self.fail('Should have raised Http404')


class SitemapTestCase(TestCase):
    """ Ensure sitemap.xml is correct """

    def setUp(self):
        self.site1 = Site.objects.create(domain='site1.test.com')
        self.site2 = Site.objects.create(domain='site2.test.com')

        self.article_type = ResourceType.objects.create(name='article')
        self.event_type = ResourceType.objects.create(name='event')

    def test_sitemap_correct(self):
        # Set up
        now = datetime.datetime.now()

        excluded_article = Resource.objects.create(slug='excluded-article', type=self.article_type, available_on=now)
        models.SiteResource.objects.create(site=self.site1, resource=excluded_article)
        included_article1 = Resource.objects.create(slug='included-article1', type=self.article_type, available_on=now)
        models.SiteResource.objects.create(site=self.site1, resource=included_article1)
        models.SiteResource.objects.create(site=self.site2, resource=included_article1)
        included_article2 = Resource.objects.create(slug='included-article2', type=self.article_type, available_on=now)

        request = HttpRequest()
        request.site = self.site2  # sitemap should exclude site1 articles
        request.META['SERVER_NAME'] = 'test.com'
        request.META['SERVER_PORT'] = 80

        # Run
        response = views.sitemap(request)

        # Test
        self.assertEqual(response['Content-Type'], 'application/xml; charset=UTF-8')

        root = ElementTree.fromstring(response.content)
        self.assertEqual(len(root), 2)

        content = str(response.content, 'utf-8')
        self.assertTrue(excluded_article.slug not in content)
        self.assertTrue(included_article1.slug in content)
        self.assertTrue(included_article2.slug in content)
