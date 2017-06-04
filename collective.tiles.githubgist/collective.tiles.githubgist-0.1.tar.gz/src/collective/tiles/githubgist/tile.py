# -*- coding: utf-8 -*-
"""Tile implementation."""

# zope imports
from plone import tiles
from plone.app.standardtiles import _PMF
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.supermodel.model import Schema
from plone.tiles.directives import ignore_querystring
from zope import schema
from zope.component import queryUtility

# local imports
from collective.tiles.githubgist import _


class IGithubGistTile(Schema):
    """A tile that shows Gists from GitHub."""

    tile_title = schema.TextLine(
        description=_PMF(
            u'The title will also be used to create identifying class on '
            u'that tile'
        ),
        required=True,
        title=_PMF(u'Title'),
    )

    show_title = schema.Bool(
        default=True,
        title=_PMF(u'Show tile title'),
    )

    ignore_querystring('html_snippet')
    gist_url = schema.TextLine(
        title=_(u'Github Gist URL'),
        required=True,
    )


class GithubGistTile(tiles.Tile):
    """A tile that shows Gists from GitHub."""

    @property
    def tile_id(self):
        return queryUtility(IIDNormalizer).normalize(
            self.data.get('tile_title')
        )

    @property
    def tile_title(self):
        return self.data.get('tile_title')

    @property
    def show_title(self):
        return self.data.get('show_title')

    @property
    def gist_url(self):
        return u'{0}.js'.format(
            self.data.get('gist_url')
        )
