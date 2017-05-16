#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Contentful API
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Contentful API.
#
# Hive Contentful API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Contentful API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Contentful API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

class EntryApi(object):

    def list_entries(self, space = None):
        space = space or self.space
        url = self.base_url + "spaces/%s/entries" % space
        contents = self.get(url)
        return contents

    def get_entry(self, id, space = None):
        space = space or self.space
        url = self.base_url + "spaces/%s/entries/%s" % (space, id)
        contents = self.get(url)
        return contents
