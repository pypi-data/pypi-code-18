"""
Copyright (2017) Raydel Miranda 

This file is part of Django-S3.

    Django-S3 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Django-S3 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Django-S3.  If not, see <http://www.gnu.org/licenses/>.
"""

import pytest
import mock

from django_s3.browser import Browser

@pytest.mark.usefixtures('paths')
class TestBrowser:
    def test_build_jason(self, paths):
        expected_structure = {
            'root': {
                'children': [
                    {
                        'name': "GRAPHIC-RESOURCES",
                        'type': "FOLDER",
                        'children': [
                            {
                                'name': 'BACKGROUNDS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'CLIPPING-FLOWERS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'CUSTOM-PRODUCTS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'CUSTOMIZABLE-PRODUCTS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'GIFTS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'LINE-PRODUCTS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'RESOURCE-COMPOSITIONS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'VASES-WITH-BACKGROUNDS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'VASES',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'WRAPPING_FLOWERS',
                                'type': 'FOLDER'
                            },
                        ]
                    },
                    {
                        'name': "EXAMPLE",
                        'type': "FOLDER",
                        'children': [
                            {
                                'name': 'example.txt',
                                'type': 'FILE'
                            }
                        ]
                    },
                    {
                        'name': "RAW-PICTURES",
                        'type': "FOLDER",
                        'children': [
                            {
                                'name': 'BACKGROUNDS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'GIFTS',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'PRODUCTS',
                                'type': 'FOLDER',
                                'children': [
                                    {
                                        'name': 'CR01',
                                        'type': 'FOLDER'
                                    },
                                    {
                                        'name': 'CR02',
                                        'type': 'FOLDER'
                                    },
                                    {
                                        'name': 'CR03',
                                        'type': 'FOLDER'
                                    }
                                ]
                            },
                            {
                                'name': 'VASES',
                                'type': 'FOLDER'
                            },
                            {
                                'name': 'WRAPPING-FLOWERS',
                                'type': 'FOLDER'
                            }
                        ]
                    },

                ]
            }
        }
        browser = Browser()
        assert browser.walk() == expected_structure, \
            "The structure for the folders is not correct."

    def test_browser_get_structure_relative(self, paths):
        browser = Browser()
        assert browser.walk('EXAMPLE') == [{'name': 'example.txt', 'type': 'FILE'}], \
            "walk function with parameter returns the structure relative to the folder"
