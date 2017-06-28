# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from grymp.processors.feature import Feature


class TestFeature(unittest.TestCase):

    def test_translate_name_no_year(self):
        with self.assertRaises(ValueError):
            Feature.translate_name('foobar')

    def test_translate_name_substitution(self):
        self.assertEqual(Feature.translate_name(
            'Dont.Foo.2222.Bluray.1080p.DTS-HD.x264-Grym'),
                         'Don\'t Foo')

    def test_translate_name_dash(self):
        self.assertEqual(Feature.translate_name(
            'Foo.Bar-Baz.Bat.2245.Bluray.1080p.DTS-HD.x264-Grym'),
                         'Foo Bar - Baz Bat')

    def test_translate_name_dot(self):
        self.assertEqual(Feature.translate_name(
            'Foo.Bar.Baz.1995.Bluray.1080p.DTS-HD.x264-Grym'),
                         'Foo Bar Baz')
