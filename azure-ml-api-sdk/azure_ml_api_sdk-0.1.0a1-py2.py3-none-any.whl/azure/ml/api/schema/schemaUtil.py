# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
"""
Utilities to save and load heterogeneous schema and type dictionary, also used
to parse http input using the schema and type dictionary
"""

import json
import os.path

from azure.ml.api.schema.sampleDefinition import SampleDefinition
from azure.ml.api.exceptions.BadRequest import BadRequestException
from azure.ml.api.exceptions.InternalServerError import InternalServerException
from azure.ml.api.schema.schemaObjects import Schema, ServiceSchema
from azure.ml.api.schema.dataTypes import DataTypes


def save_service_schema(file_path, input_schema_sample=None, output_schema_sample=None):
    if file_path is None or len(file_path) == 0:
        raise ValueError("A file path for the schema must be specified")
    target_dir = os.path.dirname(file_path)
    if len(target_dir) > 0 and not os.path.exists(target_dir):
        raise ValueError("Please specify a valid path to save the schema file to")
    if input_schema_sample is None and output_schema_sample is None:
        raise ValueError("At least one of the input / output schema samples need to be specified on this call")

    result_dict = dict()
    if input_schema_sample is not None:
        if not isinstance(input_schema_sample, dict):
            raise ValueError("Invalid input schema sample: must be a map input name -> input definition")
        result_dict["input"] = _get_serialized_schema_dict(input_schema_sample)
    if output_schema_sample is not None:
        if not isinstance(output_schema_sample, dict):
            raise ValueError("Invalid output schema sample: must be a map output name -> output definition")
        result_dict["output"] = _get_serialized_schema_dict(output_schema_sample)

    try:
        with open(file_path, 'w') as outfile:
            json.dump(result_dict, outfile)
    except:
        print("Failed to save schema file")
        raise


def load_service_schema(filename):
    if filename is None:
        raise TypeError('A filename must be specified.')
    if not os.path.exists(filename):
        raise ValueError('Specified schema file cannot be found: {}.'.format(filename))
    with open(filename, 'r') as outfile:
        schema_document = json.load(outfile)

    input_schema = None
    if "input" in schema_document:
        input_schema = _get_deserialized_schema_dict(schema_document["input"])
    output_schema = None
    if "output" in schema_document:
        output_schema = _get_deserialized_schema_dict(schema_document["output"])
    return ServiceSchema(input_schema, output_schema)


def _validate_inputs(input_dict, schema, defaults):
    if type(input_dict) != dict:
        raise BadRequestException("Input request is not in format as specified by swagger")
    for key in schema.keys():
        if key not in input_dict and key not in defaults:
            raise BadRequestException("Argument mismatch: Run function takes in an argument {0} "
                                      "which is not present in inputs".format(key))


def parse_service_input(http_body, service_input_schema, defaults):
    if service_input_schema is None:
        raise InternalServerException("service schema is set to None")
    if defaults is None:
        raise InternalServerException("defaults is set to None")
    input_json = json.loads(http_body)
    run_input = dict()
    _validate_inputs(input_json, service_input_schema, defaults)
    for input_name, raw_input_value in input_json.items():
        input_schema = service_input_schema[input_name]
        if isinstance(input_schema, Schema):
            try:
                if input_schema.type is DataTypes.NUMPY:
                    from azure.ml.api.schema.numpyUtil import NumpyUtil
                    parsed_input_value = NumpyUtil.get_input_object(raw_input_value, input_schema)
                elif input_schema.type is DataTypes.SPARK:
                    from azure.ml.api.schema.sparkUtil import SparkUtil
                    parsed_input_value = SparkUtil.get_input_object(raw_input_value, input_schema)
                elif input_schema.type is DataTypes.PANDAS:
                    from azure.ml.api.schema.pandasUtil import PandasUtil
                    parsed_input_value = PandasUtil.get_input_object(raw_input_value, input_schema)
                elif input_schema.type is DataTypes.STANDARD:
                    from azure.ml.api.schema.pythonUtil import PythonUtil
                    parsed_input_value = PythonUtil.get_input_object(raw_input_value, input_schema)
                else:
                    raise ValueError("Invalid schema type found: {}. Only types defined in dataTypes.DataTypes are "
                                     "valid".format(input_schema.type))
                run_input[input_name] = parsed_input_value
            except ValueError as ex:
                raise BadRequestException("Failed to deserialize {0} to type provided by input schema, Error Details: "
                                          "{1}".format(input_name, str(ex)))
        else:
            raise InternalServerException("Bad input type detected: {0}".format(type(input_schema)))
    return run_input


def parse_batch_input(input_file, input_schema, has_header):
    try:
        if input_schema.type is DataTypes.NUMPY:
            from azure.ml.api.schema.numpyUtil import NumpyUtil
            parsed_input_value = NumpyUtil.get_input_object_from_file(input_file, input_schema, has_header)
        elif input_schema.type is DataTypes.SPARK:
            from azure.ml.api.schema.sparkUtil import SparkUtil
            parsed_input_value = SparkUtil.get_input_object_from_file(input_file, input_schema, has_header)
        elif input_schema.type is DataTypes.PANDAS:
            from azure.ml.api.schema.pandasUtil import PandasUtil
            parsed_input_value = PandasUtil.get_input_object_from_file(input_file, input_schema)
        elif input_schema.type is DataTypes.STANDARD:
            from azure.ml.api.schema.pythonUtil import PythonUtil
            parsed_input_value = PythonUtil.get_input_object_from_file(input_file, input_schema)
        else:
            raise ValueError("Invalid schema type found: {}. Only types defined in dataTypes.DataTypes are "
                             "valid".format(input_schema.type))
    except ValueError as ex:
        raise BadRequestException("Failed to deserialize {0} to type provided by input schema, Error Details: "
                                  "{1}".format(input_file, str(ex)))
    return parsed_input_value


def _get_serialized_schema_dict(schema):
    if schema is None:
        return
    result = dict()
    for input_key, input_value in schema.items():
        if isinstance(input_value, SampleDefinition):
            result[input_key] = input_value.serialize()
        else:
            raise ValueError("Invalid Schema: Bad input type detected for argument {0}, input schema only supports " 
                             "types or Sample Definition objects, found {1}".format(input_key, type(input_value)))
    return result


def _get_deserialized_schema_dict(schema):
    result = dict()
    for input_key, input_value in schema.items():
        if "type" not in input_value or input_value["type"] is None:
            raise ValueError("Invalid schema, type not found for item {0}".format(input_key))
        if "internal" not in input_value or input_value["internal"] is None:
            raise ValueError("Invalid schema, internal schema not found for item {0}".format(input_key))
        if "swagger" not in input_value or input_value["swagger"] is None:
            raise ValueError("Invalid schema, swagger not found for item {0}".format(input_key))

        data_type = input_value["type"]
        serialized_schema = input_value["internal"]
        if data_type is DataTypes.NUMPY:
            from azure.ml.api.schema.numpyUtil import NumpySchema
            internal_schema = NumpySchema.deserialize_from_string(serialized_schema)
        elif data_type is DataTypes.SPARK:
            from azure.ml.api.schema.sparkUtil import SparkSchema
            internal_schema = SparkSchema.deserialize_from_string(serialized_schema)
        elif data_type is DataTypes.PANDAS:
            from azure.ml.api.schema.pandasUtil import PandasSchema
            internal_schema = PandasSchema.deserialize_from_string(serialized_schema)
        elif data_type is DataTypes.STANDARD:
            from azure.ml.api.schema.pythonUtil import PythonSchema
            internal_schema = PythonSchema.deserialize_from_string(serialized_schema)
        else:
            raise ValueError("Invalid schema type found: {}. Only types defined in dataTypes.DataTypes are "
                             "valid".format(data_type))
        result[input_key] = Schema(data_type, internal_schema, input_value["swagger"])
    return result
