#!/usr/bin/env python
"""
A Flask Application for searching through files in a directory.
 and uploading them to a customized s3 bucket
"""

import argparse
import os
import json
import re
import shutil
import logging
import sys

import requests
import time
# from flask import Flask
# from gooey import Gooey, GooeyParser
from pypref import Preferences
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# app = Flask(__name__)
preference = Preferences(filename="vision_config.py")


ALLOWED_FILE_EXTENSIONS = ['xml', 'csv']

FILE_TYPE_PATTERNS = {
    "NeptuneV2": "^NeptuneV2_.*\\.txt$",
    "MuellerIntervalReads": "^IntervalReads_.*\\.csv$",
    "FathomMeters": ""
}

METER_FILENAME_PATTERN = [
    "^MeterDataExchange_.*\\.csv$",  # Mueller
    "^NeptuneV2_.*\\.txt$",          # Neptune
    "^Readings_Installs_.*\\.csv.*",  # Aclara
    "^FathomMeters_.*\\.csv$",       # No particular vendor
    "^AdvancedMeters_.*\\.csv$"      # AdvancedMeters
]
READS_FILENAME_PATTERN = [
    "^IntervalReads_.*\\.csv$",      # Mueller
    "^Reads.*\\.csv$",               # Mueller or Itron?
    "^Readings_Readings_.*\\.csv.*",  # Aclara
    "^FathomReads.*\\.csv$"          # No particular vendor
]
ACCOUNTS_FILENAME_PATTERN = [
    "^.*\\.hdl\\.\\d{14}.*\\.csv$",  # Remove this
    "^AdvancedAccountMeters_.*\\.csv$"  # AdvancedAccountMeters
]


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "upload_error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "upload.log"), "w")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def check_is_meters_file(filename):
    meters_reg_match = any(re.match(regex_str, filename) for regex_str in METER_FILENAME_PATTERN)
    return meters_reg_match


def check_is_reads_file(filename):
    reads_reg_match = any(re.match(regex_str, filename) for regex_str in READS_FILENAME_PATTERN)
    return reads_reg_match


def check_is_accounts_file(filename):
    accounts_reg_match = any(re.match(regex_str, filename) for regex_str in ACCOUNTS_FILENAME_PATTERN)
    return accounts_reg_match


def check_file_type(filename):
    file_type = None
    if check_is_meters_file(filename):
        file_type = 'Meters'
        return file_type
    elif check_is_reads_file(filename):
        file_type = 'Reads'
        return file_type
    elif check_is_accounts_file(filename):
        file_type = 'Accounts'
        return file_type
    else:
        file_type = 'Others'
        return file_type


def check_file_extension_type(filename):
    """
    Check for accepted File Extension Types
    """
    file_extension = os.path.splitext(filename)[1][1:].lower()
    if file_extension:
        for ext in ALLOWED_FILE_EXTENSIONS:
            if file_extension in ext:
                return file_extension


def get_selected_file_name_without_date(filename):
    """
    Extract file name without the date prefixed or suffixed to it
    """
    file_name = filename.split('.')[0]
    date_in_filename = re.search(r'[0-9]{2,4}[\/,:\-][0-9]{2}[\/,:\-][0-9]{2,4}', file_name)
    try:
        only_date = date_in_filename.group()
        only_file_name = file_name.strip(only_date)
        return only_file_name
    except Exception:
        logging.info("No date in %s" % filename)
        return filename


def check_if_directory(directory):
    """
    Check if directory exists
    """
    if not os.path.isdir(directory):
        raise IOError("Not a directory")
    return directory


def check_if_bucket_in_s3(connection, bucket_name):
    """
    Finds existing bucket using the directory name
    in s3 or creates a new one if none exists
    """
    if connection.lookup(bucket_name) is None:
        logging.info("Creating a new S3 Bucket")
        bucket = connection.create_bucket(bucket_name)
        logging.info("S3 bucket %s created" % bucket_name)
    else:
        logging.info("Found bucket %s" % bucket_name)
        bucket = bucket_name
    return bucket


def authenticate_with_cred(client_name, fathom_token):
    url = 'http://com-gwfathom-fsh-dev.us-west-2.elasticbeanstalk.com/Vision/ValidateCredentials'
    request_body = {
        'clientName': client_name,
        'tokenString': fathom_token
    }
    headers = {'content-type': 'application/json'}
    response = requests.post(url, data=json.dumps(request_body), headers=headers)
    if response.status_code == 200:
        return True
    else:
        logging.error(response.json()['message'])


def get_s3_signed_url(filename, directory_path, client_name, file_type):
    # get PresignedUrl
    url = 'http://localhost:5000/Vision/InitiateFileUpload'
    payload = {
        "filename": filename,
        "clientName": client_name}
    headers = {'content-type': 'application/json'}
    get_jobid_and_puturl = requests.post(url, data=json.dumps(payload), headers=headers)
    response = get_jobid_and_puturl.json()
    logging.info('Status Code %s' % get_jobid_and_puturl.status_code)
    put_url = response["putUrl"]
    job_id = response["fileId"]

    # make a post request to putUrl
    # that is gotten from above with file path to be uploaded
    with open(os.path.join(directory_path, filename), 'r') as file_path_data:
        requests.put(put_url, data=file_path_data)
    try:
        time.sleep(2)
        # Implement Send job to sqs
        processurl = 'http://localhost:5000/Vision/ProcessFile'
        process_pay_load = {"fileId": job_id}
        start_job = requests.post(processurl, data=json.dumps(process_pay_load), headers=headers)
        if start_job.status_code == 200:
            logging.info("Work started successfully!")
        else:
            logging.info("Work did not start!")
    except Exception as e:
        logging.error(e)


def upload_s3(directory_path, doc_type, muni, archive_dir):
    """
    Upload to s3
    """
    if check_if_directory(directory_path):
        if check_if_directory(archive_dir):
            for file in os.listdir(directory_path):
                try:
                    # Upload to S3
                    file_type = check_file_type(file)
                    upload_detail = get_s3_signed_url(file, directory_path, muni, file_type)
                    logging.info(upload_detail)
                    try:
                        shutil.move(directory_path + '/' + file, archive_dir)
                        logging.info("File %s moved from %s  to %s" % (file, directory_path, archive_dir))
                    except TypeError as e:
                        logging.info(e)
                # error handling
                except Exception as error:
                    logging.error("File not uploaded to S3 error - %s" % error)
        else:
            logging.error("Archive directory does not exist")


def create_config_file(directory, client_name, token_string, archive_dir, doc_type):
    pref_dict = {
        "DIRECTORY": directory,
        "CLIENT_NAME": client_name,
        "TOKEN_STRING": token_string,
        "ARCHIVE_DIR": archive_dir,
        "DOC_TYPE": doc_type}
    return preference.set_preferences(pref_dict)


def check_preference_exist():
    status, message = preference.check_preferences(preference)
    return status


def update_config(directory, client_name, token_string, archive_dir, doc_type):
    update_dict = {
        "DIRECTORY": directory,
        "CLIENT_NAME": client_name,
        "TOKEN_STRING": token_string,
        "ARCHIVE_DIR": archive_dir,
        "DOC_TYPE": doc_type}
    return preference.update_preferences(update_dict)


class UploadHandler(FileSystemEventHandler):
    """ Runs the Upload Function when Watchdog calls this modified event on the watch directory"""
    def __init__(self, directory, doc_type, client_name, archive_dir):
        self.directory = directory
        self.doc_type = doc_type
        self.client_name = client_name
        self.archive_dir = archive_dir

    def on_modified(self, event):
        upload_s3(
            self.directory,
            self.doc_type,
            self.client_name,
            self.archive_dir
        )


# @Gooey()
def main():
    """
    Main function that gets args from the gooey GUI
    """
    initialize_logger('')
    # parser = GooeyParser(description='Upload files to s3')
    parser = argparse.ArgumentParser()
    stored_args = {}
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    args_file = "{}-args.json".format(script_name)
    if os.path.isfile(args_file):
        with open(args_file) as data_file:
            stored_args = json.load(data_file)

    if preference.get("DIRECTORY") is None:
        parser.add_argument(
            '-d', '--directory',
            action='store',
            default=stored_args.get('directory'),
            help='Directory that contains files to be watched',
            required=True)
        parser.add_argument(
            '-cn', '--client_name',
            action='store',
            default=stored_args.get('client_name'),
            help='The client_name to which the document applies, from the configuration',
            required=True)
        parser.add_argument(
            '-ft', '--fathom_token',
            action='store',
            default=stored_args.get('fathom_token'),
            help='Fathom authentication token...gotten from the View system',
            required=True)

        parser.add_argument(
            '-ad', '--archive_dir',
            action='store',
            default=stored_args.get('archive_dir'),
            help='Directory that files will be moved into after upload',
            required=True)

        parser.add_argument('doc_type', choices=['xml', 'csv'], default='xml', nargs='?')

        args = parser.parse_args()

        doc_type = args.doc_type

        directory = args.directory
        client_name = args.client_name
        fathom_token = args.fathom_token
        archive_dir = args.archive_dir
        directory_path, directory_name = os.path.split(directory)
        logging.info("Directory %s found!" % directory_name)
        if authenticate_with_cred(client_name, fathom_token):
            create_config_file(directory, client_name, fathom_token, archive_dir, doc_type)
            logging.info("Saved config to vision_config.py")
        else:
            logging.error("Please enter the correct credentials")
            sys.exit(0)
    doc_type = preference.get("DOC_TYPE")
    directory = preference.get("DIRECTORY")
    client_name = preference.get("CLIENT_NAME")
    fathom_token = preference.get("TOKEN_STRING")
    archive_dir = preference.get("ARCHIVE_DIR")
    directory_path, directory_name = os.path.split(directory)

    if authenticate_with_cred(client_name, fathom_token):
        # Upload mthod runs first and ships all files to s3
        upload_s3(directory, doc_type, client_name, archive_dir)
        event_handler = UploadHandler(directory, doc_type, client_name, archive_dir)
        observer = Observer()
        observer.schedule(event_handler, path=directory, recursive=True)
        # Watch dog starts observing new files added to the monitored directory
        observer.start()
        try:
            while True:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

if __name__ == '__main__':
    main()
