"""
Copyright (2017) Raydel Miranda Gomez 

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

from django.conf import settings
import boto


class Browser(object):
    def __init__(self):
        self.__structure = {}
        # Connect to the bucket
        self.__conn = boto.connect_s3(
            aws_access_key_id=settings.S3_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.S3_AWS_SECRET_ACCESS_KEY
        )
        self.__bucket = self.__conn.get_bucket(settings.BUCKET_NAME)
        self.__files = self.__bucket.list()

    def __build_structure(self):
        pass

    def walk(self, relative_to="/"):
        pass
