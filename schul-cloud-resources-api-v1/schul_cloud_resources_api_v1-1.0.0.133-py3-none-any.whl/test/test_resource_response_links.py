# coding: utf-8

"""
    Schul-Cloud Content API

    This is the specification fo rthe content of Schul-Cloud. You can find more information in the [repository](https://github.com/schul-cloud/resources-api-v1). 

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from __future__ import absolute_import

import os
import sys
import unittest

import schul_cloud_resources_api_v1
from schul_cloud_resources_api_v1.rest import ApiException
from schul_cloud_resources_api_v1.models.resource_response_links import ResourceResponseLinks


class TestResourceResponseLinks(unittest.TestCase):
    """ ResourceResponseLinks unit test stubs """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testResourceResponseLinks(self):
        """
        Test ResourceResponseLinks
        """
        model = schul_cloud_resources_api_v1.models.resource_response_links.ResourceResponseLinks()


if __name__ == '__main__':
    unittest.main()
