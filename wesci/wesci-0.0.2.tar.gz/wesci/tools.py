import csv
import json
import time
import types
import uuid


class Logger(object):
    DEFAULT_INPUT_PARAMS_NAME = 'input_params'
    DEFAULT_INPUT_FILES_NAME = 'input_files'
    DEFAULT_OUTPUT_PARAMS_NAME = 'output_params'
    DEFAULT_OUTPUT_FILES_NAME = 'output_files'

    def __init__(self,
                 user_id,
                 input_params={},
                 input_files={},
                 output_params={},
                 output_files={},
                 script_file=None):
        super(Logger, self).__init__()

        self.user_id = user_id
        self.input_params = Logger.__convert_arg_to_hash(
            input_params,
            self.DEFAULT_INPUT_PARAMS_NAME
        )
        self.input_files = Logger.__convert_arg_to_hash(
            input_files,
            self.DEFAULT_INPUT_FILES_NAME
        )
        self.output_params = Logger.__convert_arg_to_hash(
            output_params,
            self.DEFAULT_OUTPUT_PARAMS_NAME
        )
        self.output_files = Logger.__convert_arg_to_hash(
            output_files,
            self.DEFAULT_OUTPUT_FILES_NAME
        )
        self.file_name = script_file
        self.code = Logger.__get_code_from_file(script_file)
        self.run_id = Logger.__generate_run_id()

    def log(self):
        csv_row = self.__csv_row_data()
        CSVSaver.save(csv_row)

    @staticmethod
    def __convert_arg_to_hash(arg, name):
        if isinstance(arg, types.DictionaryType):
            return arg
        return {name: arg}

    @staticmethod
    def __generate_run_id():
        # composed of millisecond epoch an a standard UUID
        time_now = int(time.time() * 1000)
        uid = uuid.uuid4().hex
        run_id = "%s_%s" % (time_now, uid)
        return run_id

    @staticmethod
    def __get_code_from_file(script_file):
        if script_file is None:
            return None
        return open(script_file).read()

    def __print_params(self):
        print "logged for user %s" % self.user_id
        print "logged the following input params: %s" % self.input_params
        print "logged the following input files: %s" % self.input_files
        print "logged the following output params: %s" % self.output_params
        print "logged the following output files: %s" % self.output_files
        print "run id is %s" % self.run_id

    def __csv_row_data(self):
        return [
            self.user_id,
            self.run_id,
            json.dumps(self.input_params),
            json.dumps(self.input_files),
            json.dumps(self.output_params),
            json.dumps(self.output_files),
            self.file_name,
            self.code
        ]


class CSVSaver(object):
    FILE_PATH = 'wesci_log.csv'

    @staticmethod
    def save(csv_row):
        with open(CSVSaver.FILE_PATH, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
