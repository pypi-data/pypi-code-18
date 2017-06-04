#!/usr/bin/env python3
# vim:fileencoding=utf-8
#
# Spotify2MusicBrainz: Submit data from Spotify to MusicBrainz
# Copyright © 2016–2017 Frederik “Freso” S. Olesen <https://freso.dk/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
""""""

from pkg_resources import get_distribution, DistributionNotFound, RequirementParseError
try:
    __version__ = get_distribution(__name__).version
except (DistributionNotFound, RequirementParseError):
    # not installed as package or is being run from source/git checkout
    from setuptools_scm import get_version
    __version__ = get_version()

import os
import tempfile
import webbrowser
from collections import namedtuple
from functools import lru_cache
from urllib.parse import urlparse

import musicbrainzngs
import spotipy

musicbrainzngs.set_useragent("Spotify2MusicBrainz", __version__,
                             "https://gitlab.com/Freso/spotify2musicbrainz")

MUSICBRAINZ_SERVER = "https://musicbrainz.org"
HTML_HEAD = """<!doctype html>
<meta charset="UTF-8">
<title>%s</title>
<form action="%s" method="post">
"""
HTML_INPUT = """<input type="hidden" name="%s" value="%s">
"""
HTML_TAIL = """<input type="submit" value="%s">
</form>
<script>document.forms[0].submit()</script>
"""
EDIT_NOTE = """Imported from Spotify using Spotify2MusicBrainz: https://gitlab.com/Freso/spotify2musicbrainz

Information fetched from Spotify API URL %s"""
SPOTIFY_MUSICBRAINZ_MAPPING = {
    "album": "release",
    "artist": "artist",
    "track": "recording",
}


def make_spotify_tuple(url):
    """Take a Spotify URL string and turn it into a (named) tuple.

    >>> make_spotify_tuple("http://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL")
    SpotifyIdentifier(Type='album', ID='2QE5TZ3P547etzfMWgE8lL')
    >>> make_spotify_tuple("spotify:album:2QE5TZ3P547etzfMWgE8lL")
    SpotifyIdentifier(Type='album', ID='2QE5TZ3P547etzfMWgE8lL')
    >>> make_spotify_tuple("ftp://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL")
    Traceback (most recent call last):
        ...
    ValueError: ftp://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL is not a recognized Spotify URL.
    """
    SpotifyIdentifier = namedtuple("SpotifyIdentifier", ["Type", "ID"])
    parsed_url = urlparse(url)

    if parsed_url.scheme in ("http", "https"):
        return SpotifyIdentifier._make(parsed_url.path.strip("/").split("/"))
    elif parsed_url.scheme in ("spotify"):
        return SpotifyIdentifier._make(parsed_url.path.split(":"))
    else:
        raise ValueError("%s is not a recognized Spotify URL." % url)


def validate_spotify_id(spotify_id):
    """Validate Spotify IDs.

    >>> validate_spotify_id("2QE5TZ3P547etzfMWgE8lL")
    True
    >>> validate_spotify_id("Æøå")
    False
    """
    import re
    return not re.search("[^0-9A-Za-z]", spotify_id)


def make_spotify_url(spotify_id, spotify_type="album"):
    """Generate a Spotify URL from data.

    >>> make_spotify_url("2QE5TZ3P547etzfMWgE8lL")
    'https://open.spotify.com/album/2QE5TZ3P547etzfMWgE8lL'
    >>> make_spotify_url("2QE5TZ3P547etzfMWgE8lL", "artist")
    'https://open.spotify.com/artist/2QE5TZ3P547etzfMWgE8lL'
    >>> make_spotify_url("Æøå")
    Traceback (most recent call last):
        ...
    ValueError: "Æøå" is not a valid Spotify ID.
    >>> make_spotify_url("2QE5TZ3P547etzfMWgE8lL", "tinny word")
    Traceback (most recent call last):
        ...
    ValueError: "tinny word" is not a recognized Spotify entity type.
    """
    if not validate_spotify_id(spotify_id):
        raise ValueError('"%s" is not a valid Spotify ID.' % spotify_id)
    if spotify_type not in SPOTIFY_MUSICBRAINZ_MAPPING:
        raise ValueError('"%s" is not a recognized Spotify entity type.' % spotify_type)
    return "https://open.spotify.com/{0}/{1}".format(spotify_type, spotify_id)


@lru_cache(maxsize=None)
def get_spotify_instance():
    "Create and return an authorized Spotify client instance."
    from spotipy.oauth2 import SpotifyClientCredentials

    credentials = SpotifyClientCredentials(
        client_id='185da831f8884c61893cbea03b5933a9',
        client_secret='87cdaf22222649b496abc598d4126b01')
    return spotipy.Spotify(client_credentials_manager=credentials)


@lru_cache(maxsize=None)
def get_spotify_album_data(spotify_id):
    spotify = get_spotify_instance()
    album = spotify.album(spotify_id)
    tracks = album["tracks"]["items"]
    while album["tracks"]["next"]:
        album["tracks"] = spotify.next(album["tracks"])
        tracks.extend(album["tracks"]["items"])
    album["tracks"]["items"] = tracks
    return album


@lru_cache(maxsize=None)
def get_artist_mbid(spotify_id):
    spotify_url = make_spotify_url(spotify_id, "artist")
    try:
        mb_url = musicbrainzngs.browse_urls(spotify_url,
                                            includes=["artist-rels"])
    except musicbrainzngs.musicbrainz.ResponseError:
        # TODO: Raise appropriate exception. (URL doesn't exist.)
        return None

    if "artist-relation-list" in mb_url["url"]:
        artists = mb_url["url"]["artist-relation-list"]
        if len(artists) == 1:
            return artists[0]["artist"]["id"]
        elif len(artists) > 1:
            # TODO: Raise appropriate exception. (More than one associated artist.)
            return None
    else:
        # TODO: Raise appropriate exception. (No associated artists.)
        return None


def mbserver_url(path):
    return MUSICBRAINZ_SERVER + path


class AddObjectAsEntity(object):
    NAME = "Add Object As Entity..."
    objtype = None
    submit_path = "/"

    def __init__(self):
        super(AddObjectAsEntity, self).__init__()
        self.form_values = {}

    def check_object(self, objs, objtype):
        """
        Checks if a given object array is valid (ie., has one item) and that
        its item is an object of the given type.

        Returns either False (if conditions are not met), or the object in the
        array.
        """
        if not isinstance(objs[0], objtype) or len(objs) != 1:
            return False
        else:
            return objs[0]

    def add_form_value(self, key, value):
        "Add global (e.g., release level) name-value pair."
        self.form_values[key] = value

    def set_form_values(self, objdata):
        return

    def generate_html_file(self, form_values):
        """Generate HTML file for submitting information to MusicBrainz."""
        (fd, fp) = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            def esc(s):
                """Escape HTML entities."""
                import html
                return html.escape(s, quote=True)

            def nv(n, v):
                """Write global/release level name-value pair to HTML file."""
                f.write(HTML_INPUT % (esc(n), esc(v)))

            f.write(HTML_HEAD % (self.NAME, mbserver_url(self.submit_path)))

            for key in form_values:
                nv(key, form_values[key])

            f.write(HTML_TAIL % (self.NAME))
        return fp

    def open_html_file(self, fp):
        webbrowser.open("file://" + fp)

    def callback(self, objs):
        objdata = self.check_object(objs, self.objtype)
        try:
            if objdata:
                self.set_form_values(objdata)
                html_file = self.generate_html_file(self.form_values)
                self.open_html_file(html_file)
        finally:
            self.form_values.clear()


class AddSpotifyAlbumAsRelease(AddObjectAsEntity):
    NAME = "Add Spotify Album As Release..."
    submit_path = "/release/add"

    def __init__(self, spotify_id):
        self.form_values = {}
        self.spotify_id = spotify_id

    def set_form_values(self, data):
        nv = self.add_form_value

        nv("artist_credit.names.0.name", data["artists"][0]["name"])
        release_artist_mbid = get_artist_mbid(data["artists"][0]["id"])
        if release_artist_mbid is not None:
            nv("artist_credit.names.0.mbid", release_artist_mbid)
        nv("name", data["name"])
        nv("urls.0.url", data["external_urls"]["spotify"])
        nv("urls.0.link_type", "85")  # "stream for free"
        nv("mediums.0.format", "Digital Media")
        nv("packaging", "None")
        if "upc" in data["external_ids"]:
            nv("barcode", data["external_ids"]["upc"])
        if "label" in data:
            nv("labels.0.name", data["label"])

        nv("edit_note", EDIT_NOTE % (data["href"]))

        for track in data["tracks"]["items"]:
            i = int(track["track_number"]) - 1

            # add a track-level name-value
            def tnv(n, v):
                nv("mediums.0.track.%d.%s" % (i, n), v)

            tnv("name", track["name"])
            if track["artists"][0]["name"] != data["artists"][0]["name"] or\
               track["artists"][0]["id"] != data["artists"][0]["id"]:
                tnv("artist_credit.names.0.name", track["artists"][0]["name"])
                track_artist_mbid = get_artist_mbid(track["artists"][0]["id"])
                if track_artist_mbid is not None:
                    tnv("artist_credit.names.0.mbid", track_artist_mbid)
            tnv("length", str(track["duration_ms"]))

    def callback(self):
        objdata = get_spotify_album_data(self.spotify_id)
        try:
            if objdata:
                self.set_form_values(objdata)
                html_file = self.generate_html_file(self.form_values)
                self.open_html_file(html_file)
        finally:
            self.form_values.clear()


def get_spotify_cover_art(spotify_id):
    "Get cover art details from Spotify's Web API."
    from operator import itemgetter

    album_data = get_spotify_album_data(spotify_id)
    images = album_data['images']
    return max(images, key=itemgetter('height'))


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("spotify_uri", type=str,
                        help="Spotify URI for the album to import")
    args = parser.parse_args()
    album = AddSpotifyAlbumAsRelease(args.spotify_uri)
    album.callback()
    print(
        'Consider also uploading cover art to the Cover Art Archive:',
        get_spotify_cover_art(args.spotify_uri)['url']
    )


if __name__ == "__main__":
    main()
