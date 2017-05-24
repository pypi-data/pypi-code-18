# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
import json
import os.path
from azure.ml.api.realtime.swagger_spec_generator import generate_service_swagger


class SwaggerGenerationTests(unittest.TestCase):
    def test_swagger_generation(self):
        test_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(test_dir, "resources/service_schema.json")
        service_name = "test_svc"
        expected_swagger_path = os.path.join(test_dir, "resources/expected_service_swagger.json")
        swagger_json = generate_service_swagger(service_name, schema_path)
        with open(expected_swagger_path, 'r') as f:
            expected_swagger_json = json.load(f)
        self.assertEqual(swagger_json, expected_swagger_json)
