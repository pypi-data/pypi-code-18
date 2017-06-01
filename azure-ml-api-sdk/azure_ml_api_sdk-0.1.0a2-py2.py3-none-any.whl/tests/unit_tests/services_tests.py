# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import shutil
import numpy as np

from azure.ml.api.realtime import services
from azure.ml.api.schema.sampleDefinition import SampleDefinition
from azure.ml.api.schema.dataTypes import DataTypes
from azure.ml.api.schema.schemaUtil import *
from tests.unit_tests.ut_common import UnitTestBase


class ServicesTests(UnitTestBase):    
    int_array = np.array(range(10), dtype=np.int32)
    input_types = {'a': SampleDefinition(DataTypes.NUMPY, int_array), 'b': SampleDefinition(DataTypes.STANDARD, 10)}
    output_types = {'output1': SampleDefinition(DataTypes.STANDARD, "Adf")}
    output_type = {"sdf": "Sdf"}

    def test_prepare_happy_path(self):
        output_folder = None
        try:
            output_folder = services.prepare(sample_run, sample_init, ServicesTests.input_types, ServicesTests.output_types, "scikit")
            self.assertTrue(os.path.exists(output_folder))
            self.assertTrue(os.path.exists(os.path.join(output_folder, "main.py")))
        finally:
            if output_folder is not None:
                shutil.rmtree(output_folder)

    def test_prepare_happy_path_with_arguments(self):
        output_folder = None
        try:
            output_folder = services.prepare(sample_run_default, sample_init, ServicesTests.input_types, ServicesTests.output_types,
                                             "scikit")
            self.assertTrue(os.path.exists(output_folder))
            self.assertTrue(os.path.exists(os.path.join(output_folder, "main.py")))
        finally:
            if output_folder is not None:
                shutil.rmtree(output_folder)

    def test_prepare_happy_path_with_no_arguments(self):
        output_folder = None
        try:
            output_folder = services.prepare(sample_run_no_args, sample_init, output_types=ServicesTests.output_types)
            self.assertTrue(os.path.exists(output_folder))
            self.assertTrue(os.path.exists(os.path.join(output_folder, "main.py")))
        finally:
            if output_folder is not None:
                shutil.rmtree(output_folder)

    def test_prepare_happy_path_with_no_arguments_and_no_output(self):
        output_folder = None
        try:
            output_folder = services.prepare(sample_run_no_args_no_output, sample_init)
            self.assertTrue(os.path.exists(output_folder))
            self.assertTrue(os.path.exists(os.path.join(output_folder, "main.py")))
        finally:
            if output_folder is not None:
                shutil.rmtree(output_folder)

    def test_prepare_no_input_schema_with_run_arguments(self):
        output_types = {'output1': str}
        self._validate_error_message_for_prepare(
            sample_run,
            sample_init,
            None,
            output_types,
            "Provided run function has arguments, input schema needs to be provided")

    def test_prepare_bad_input_type(self):
        input_types = {'a': SampleDefinition(DataTypes.NUMPY, ServicesTests.int_array)}
        output_types = {'output1': str}
        self._validate_error_message_for_prepare(
            sample_run,
            sample_init,
            input_types,
            output_types,
            "Argument mismatch: Provided run function has 2 arguments "
            "while 1 inputs were previously declared for it")

        input_types = {'a': SampleDefinition(DataTypes.NUMPY, ServicesTests.int_array), 'c':SampleDefinition(DataTypes.STANDARD, 45)}
        try:
            output_path = services.prepare(sample_run, sample_init, input_types, output_types, "scikit")
            shutil.rmtree(output_path)
            self.fail("Exception expected but none was thrown")
        except Exception as e:
            self.assertTrue("Provided run function argument b is not present in input types dictionary which contains" in str(e))

    def test_generate_bad_input_type(self):
        input_types = {'a': SampleDefinition(DataTypes.NUMPY, ServicesTests.int_array)}
        schema_file = "schema.json"
        schema_file = os.path.join(UnitTestBase.tests_folder, schema_file)
        save_service_schema(schema_file, input_types, ServicesTests.output_types)
        self._validate_error_message_for_generate_main(
            sample_run,
            sample_init,
            schema_file,
            "Argument mismatch: Provided run function has 2 arguments "
            "while 1 inputs were previously declared for it")

        input_types = {'a': SampleDefinition(DataTypes.NUMPY, ServicesTests.int_array), 'c': SampleDefinition(DataTypes.STANDARD, 5)}
        save_service_schema(schema_file, input_types, ServicesTests.output_types)
        try:
            output_path = services.generate_main(sample_run, sample_init, schema_file, "main.py")
            shutil.rmtree(output_path)
            self.fail("Exception expected but none was thrown")
        except Exception as e:
            if "Argument mismatch: Provided run function argument b is not present in input " \
               "types dictionary which contains" not in str(e):
                self.fail("Expected error message not found")
        finally:
            os.remove(schema_file)

    def test_generate_happy_path(self):
        schema_file = "schema.json"
        main_file = "main.py"
        schema_path = os.path.join(UnitTestBase.tests_folder, schema_file)
        main_path = os.path.join(UnitTestBase.tests_folder, main_file)
        try:
            save_service_schema(schema_path, ServicesTests.input_types, ServicesTests.output_types)
            services.generate_main(sample_run, sample_init, schema_path, main_path)
            self.assertTrue(os.path.exists(schema_path))
            self.assertTrue(os.path.exists(main_path))
        finally:
            if os.path.exists(schema_path):
                os.remove(schema_path)
            if os.path.exists(main_path):
                os.remove(main_path)

    def test_generate_happy_path_no_arguments(self):
        schema_file = "schema.json"
        main_file = "main.py"
        schema_path = os.path.join(UnitTestBase.tests_folder, schema_file)
        main_path = os.path.join(UnitTestBase.tests_folder, main_file)
        try:
            save_service_schema(schema_path, None, ServicesTests.output_types)
            services.generate_main(sample_run_no_args, sample_init, schema_path, main_path)
            self.assertTrue(os.path.exists(schema_path))
            self.assertTrue(os.path.exists(main_path))
        finally:
            if os.path.exists(schema_path):
                os.remove(schema_path)
            if os.path.exists(main_path):
                os.remove(main_path)

    def test_generate_no_input_schema_with_run_arguments(self):
        schema_file = "schema.json"
        schema_path = os.path.join(UnitTestBase.tests_folder, schema_file)
        save_service_schema(schema_path, None, ServicesTests.output_types)
        self._validate_error_message_for_generate_main(
            sample_run,
            sample_init,
            schema_path,
            "Provided run function has arguments, input schema needs to be provided")


    def _validate_error_message_for_prepare(self, sample_run, sample_init, input_types, output_types, message):
        try:
            output_path = services.prepare(sample_run, sample_init, input_types, output_types, "scikit")
            shutil.rmtree(output_path)
            self.fail("Exception expected but none was thrown")
        except Exception as e:
            self.assertEqual(message, str(e))

    def _validate_error_message_for_generate_main(self, sample_run, sample_init, schema_file, message):
        try:
            output_path = services.generate_main(sample_run, sample_init, schema_file, "main.py")
            shutil.rmtree(output_path)
            self.fail("Exception expected but none was thrown")
        except Exception as e:
            self.assertEqual(message, str(e))
        finally:
            os.remove(schema_file)


def sample_init():
    pass


def sample_run(a=10, **b):
    print(a)
    return b


def sample_run_no_args():
    return "asdf"


def sample_run_default(a, b=[2,3,4]):
    print(a)
    return b

def sample_run_no_args_no_output():
    print(10)
