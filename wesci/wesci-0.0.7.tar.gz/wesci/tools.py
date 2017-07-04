import csv
import json
import os
import time
import types
import uuid


class Logger(object):
    DEFAULT_INPUT_PARAMS_NAME = 'input_params'
    DEFAULT_INPUT_FILES_NAME = 'input_files'
    DEFAULT_OUTPUT_PARAMS_NAME = 'output_params'
    DEFAULT_OUTPUT_FILES_NAME = 'output_files'
    DEFAULT_LOG_PREFIX = '~/default'

    def __init__(self,
                 user_id,
                 input_params={},
                 input_files={},
                 output_params={},
                 output_files={},
                 script_file=None,
                 log_file_prefix=None):
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
        if not log_file_prefix:
            if not script_file:
                log_file_prefix=self.DEFAULT_LOG_PREFIX
            else:
                log_file_prefix=script_file
        self.log_file_prefix = os.path.expanduser(log_file_prefix)
        self.script_file = script_file
        self.code = Logger.__get_code_from_file(script_file)
        self.run_timestamp = time.time()
        self.run_id = Logger.__generate_run_id(self.run_timestamp)
        self.csv_saver = CSVSaver

    def log(self):
        csv_row = self.__csv_row_data()
        self.csv_saver.save(self.log_file_prefix, csv_row)

    @staticmethod
    def __convert_arg_to_hash(arg, name):
        if isinstance(arg, types.DictionaryType):
            return arg
        return {name: arg}

    @staticmethod
    def __generate_run_id(run_timestamp):
        # composed of millisecond epoch an a standard UUID
        ms_timestamp = int(run_timestamp * 1000)
        uid = uuid.uuid4().hex
        run_id = "%s_%s" % (ms_timestamp, uid)
        return run_id

    @staticmethod
    def __get_code_from_file(script_file):
        if script_file is None:
            return None
        return open(script_file).read() #leaked handle?

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
            time.strftime('%Y-%m-%d %H:%M:%S',
                          time.localtime(self.run_timestamp)),
            self.run_id,
            json.dumps(self.input_params),
            json.dumps(self.input_files),
            json.dumps(self.output_params),
            json.dumps(self.output_files),
            self.script_file,
            os.getcwd(),
            self.code
        ]


class CSVSaver(object):

    @staticmethod
    def __clean_file_name(file_name):
        return os.path.splitext(file_name)[0]

    @staticmethod
    def __output_file_name(log_file_prefix):
        return "%s_wesci_log.csv" % CSVSaver.__clean_file_name(log_file_prefix)

    @staticmethod
    def save(log_file_prefix, csv_row):
        output_file_name = CSVSaver.__output_file_name(log_file_prefix)
        with open(output_file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(csv_row)
