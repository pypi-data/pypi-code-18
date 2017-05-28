import os
import time
import base64
import zipfile
import requests
import tempfile
import shutil
import numpy as np
from copy import copy
from simplejson.scanner import JSONDecodeError
from random import randint
from warnings import warn
import simplejson
from glob import glob
from datetime import timedelta


if os.environ.get("DEV") == "True":
    BASE_URL = os.getenv("CUBE_API_BASE_URL", "http://localhost:8000")
else:
    BASE_URL = os.getenv("CUBE_API_BASE_URL", "http://api.cube.ai:82")

API_KEY = None
session_override = None

def make_request(url, method, **kwargs):
    methods = {
        "GET" : get_session().get,
        "POST" : get_session().post,
        "DELETE" : get_session().delete,
        "PUT": get_session().put,
    }

    num_tries = kwargs.pop("num_tries", 10)
    message = kwargs.pop("message", None)

    from api import VERBOSE
    if VERBOSE:
        print "[Cube] Requesting to", url

    for i in range(num_tries):
        response = None
        try:
            response = methods[method](url, **kwargs)
            return validate_result(response)
        except Exception as e:
            if response is None:
                raise ValueError("There was an issue connecting to the Cube API. Drop us a line at support@cube.ai if you require further assistance.")

            import traceback
            traceback.print_exc()
            if i == num_tries-1 or response.status_code not in [502, 504]:
                raise
            else:
                if message is not None:
                    warn(message)
                else:
                    warn("Unable to complete request on try %d. Retrying..." % i)
                time.sleep(1)

def get_session():
    import logging
    check_api_key()
    
    session = session_override or requests.Session()
    session.headers.clear()
    session.headers["Authentication"] = "Basic " + API_KEY

    return session

def use_session(session):
    global session_override
    session_override = session

def set_api_key(api_key, verbose=True):
    """ Set the Cube api key for the module.

    :param api_key: Your user api key, which can be found on the Cube website (under Profile)
    :type api_key: :mod:`str`
    :param verbose: If True, the user's name is printed to :mod:`stdout`.
    :type verbose: bool
    """
    global API_KEY
    API_KEY=api_key


def get_api_key():
    """ Get the Cube api key for the module.

    :returns: A :mod:`str` which is the user's api key (assuming the key has been set using :func:`set_api_key`)
    """
    header = get_session().headers.get("Authentication")
    return header[6:]

def check_api_key():
    if not API_KEY:
        raise ValueError("API_KEY key has not been set yet.")

def get_user_id():
    """ Get the user id for the current user (identified by their api key)

    :returns: An integer value which is the current user's id
    """
    return get_user_info()["id"]

def get_user_info():
    """ Get the user id for the current user (identified by their api key)

    :returns: An integer value which is the current user's id
    """
    check_api_key()
    url = BASE_URL + "/api/v1.2/current_user"
    response = get_session().get(url)
    return validate_result(response)

def get_input_from_path(path):
    """ Produces the appropriate input for the :func:`ClassificationData.add_samples` function given a path to a local directory which contains sub-directories which are named by their desired class name. Each subdirectory should contain images or text files of the corresponding class
    """
    return [(f,os.path.split(label_dir)[1]) for label_dir in glob(os.path.abspath(path) + "/*") for f in glob(label_dir + "/*")]

def match_predictions_with_labels(predictions, file_input):
    file_input = repackage_input(file_input)

    fnames = list(zip(*file_input)[0])

    required_keys = ["user_value", "class"]
    for pred in predictions:
        for key in required_keys:
            if not pred.get(key):
                return ValueError("each dictionary in predictions must contain a '" + key + "' key")

    return [(pred["class"], file_input[fnames.index(pred["user_value"])][1]) for pred in predictions]

def validate_no_content(response):
    if response.status_code != 204:
        raise ValueError("Unexpected response (code: %d, url: %s)" % (response.status_code, response.url))

def validate_result(response):
    try:
        result=response.json()
    except JSONDecodeError:
      raise ValueError("Error converting server response to JSON. Unknown server error (error code: %d, url: %s)" % (response.status_code, response.url))

    if "message" in result.keys():
        raise ValueError(result["message"])

    return result

def is_zipfile(f):
    try:
        zipfile.ZipFile(f)
        return True
    except:
        return False

def repackage_input(input_, input_type, unzip_on_client=True):
    input_=copy(input_)
    input_type=copy(input_type)
    # some minimal repackaging
    if input_type=="zip" and unzip_on_client:
        warn("Unzipping file '%s' into a temporary directory (for higher upload speed)"%input_, UserWarning)
        tmpdir = os.path.join(tempfile.gettempdir(), str(randint(0,10000000000)))
        if not os.path.isdir(tmpdir):
            os.makedirs(tmpdir)
        zf = zipfile.ZipFile(input_)
        zf.extractall(path=tmpdir)
        root = zf.namelist()[0].encode("ascii")
        if root != "/":
            tmpdir = os.path.join(tmpdir, root)
        input_ = get_input_from_path(tmpdir)
        input_type='files'
    elif isinstance(input_, str) or isinstance(input_,unicode):
        # repackage strings
        pass
        #input_ = [(input_, None)]
    elif isinstance(input_, tuple):
        input_ = [input_]
    elif isinstance(input_, list):
        # repackage unlabeled lists
        pass
        # for i,val in enumerate(input_[:]):
        #     if not isinstance(val, tuple):
        #         input_[i] = (val, None)
    elif input_type=="numpy":
        input_ = input_.tolist()
        pass
        # for i,val in enumerate(input_[:]):
        #     if not isinstance(val, tuple):
        #         # Sub-array is numpy

        #         input_[i] = (val, None)

    else:
        raise ValueError("input_type not recognized. input_type must either be a string, tuple, or list")

    return input_,input_type

def process_input_in_batches(url, input_, input_type, unzip_on_client=False, skip_invalid_values=True, encoding='utf-8', verbose=False, secret_key=None, model_id=None, options={}):
    assert input_ is not None,"input parameter must be specified"
    assert input_type is not None,"input_type parameter must be specified"

    assert type(input_) in [list, np.ndarray], "input parameter must be list or NumPy array for batch uploads"
    
    input_repackaged, input_type_repackaged = repackage_input(input_, input_type,unzip_on_client)
    
    # build request, looping over batches of the max number of open files (minus 50)
    results = []
    max_open_files = 150

    # Split the list into chuncks
    split_input = [input_repackaged[i:i+max_open_files] for i in range(0,len(input_repackaged), max_open_files)]
    num_uploaded_files = 0

    if isinstance(input_repackaged, list):
        num_files = len(input_repackaged)
    else:
        num_files = 1
    
    for batch_num, inp in enumerate(split_input):
        files=[]
        data=[]

        # Iterate through each record
        for value in inp:
            data.append(value)

        num_uploaded_files += len(data)

        new_or_append = "append" if batch_num > 0 else "new"

        data={"entry_type": input_type_repackaged,
              "new_or_append": new_or_append,
              "skip_invalid_values": skip_invalid_values,
              "data": simplejson.dumps(data, encoding=encoding),
              "secret_key": secret_key,
              "model_id": model_id}
        data.update(options)

        result = make_request(url, 'POST', files=files, data=data)

        if result.get("skipped_values"):
            if result.get("name") and result.get("data_type"):
                warn("Skipping the following values because they were invalid for the dataset '%s' (which has the data type '%s'): %s" % (result["name"], result["data_type"], str(result["skipped_values"])))
            else:
                warn("Skipping the following values: %s" % (str(result["skipped_values"])))
        
        results.append(result)

        # close all the files
        for f in files:
            if not f[1].closed:
                f[1].close()
        if verbose: print("Finished uploading %d of %d samples..." %(num_uploaded_files, num_files))

    return results
