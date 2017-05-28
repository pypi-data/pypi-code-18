import os
import time
import requests
import json
import urllib2
import StringIO
import numpy as np
import itertools
import cPickle
import sklearn
from json import dumps, loads
from simplejson.scanner import JSONDecodeError

from .utils import check_api_key, get_session, validate_result, BASE_URL, \
                   repackage_input, process_input_in_batches, make_request, \
                   set_api_key

def process_response_json(r):
    global VERBOSE
    if VERBOSE:
        print "[Cube] Recieved Response:\n----------------------\n", r.content, "\n------------------\n"

    try:
        json_response = r.json()
    except JSONDecodeError:
        json_response = {"error_response": ""}
        if VERBOSE:
            print "[Cube] Error Decoding Returned JSON"


    if "error_type" in json_response:
        raise Exception("An %s error was obtained from the Cube API: " % json_response["error_type"] + json_response["error_message"])

    return json_response


# TODO:  Exceptions not being raised properly

# TODO: Remove code smell
ee = Exception

exception_instances = {}

class Exception(Exception):
    name = None

    def __init__(self, name=""):
        self.name = name
        # TODO: Rename classes

        self.args=["Please view more about this specific error at https://docs.cube.ai/exceptions/%s" % name ]

    # Interface that the user works with
    def __call__(self):

        Exception.make_exception(self.name)

        return exception_instances[self.name]

    @staticmethod
    def make_exception(name):
        global exception_instances
        if name not in exception_instances:
            exception_instances[name] = type(str(name), (Exception,), {})

    @staticmethod
    def merge(n1, n2):
        if not n1:
            return n2
        elif not n2:
            return n1
        else:
            return n1 + "." + n2

    def get_type_repr(self):
        return exception_instances[self.name]

    def __str__(self):
        return self.name

    def __getattr__(self, name):
        return Exception(self.merge(self.name, name))


class Cube(sklearn.base.BaseEstimator):
    secret_key = None
    model_id = None
    kind = None
    model_id = None
    requirements = None
    model_version = None
    verbose = False

    def __init__(self, model, model_id=None, secret_key=None, requirements="", kind=None, verbose=False):
        self.model = model
        self.model_id = model_id
        self.secret_key = secret_key
        self.kind = kind
        self.model_id = model_id
        self.requirements = requirements # if file, open - if string equals
        self.verbose = verbose

        global VERBOSE
        VERBOSE = verbose

        set_api_key(self.secret_key)
        
        # UNDO This:
        # create_model_if_not_exists(model=self.model, model_id=self.secret_key, secret_key=self.secret_key, requirements=self.requirements)

        # TODO: Add a cosemetic "warning Secret isn't valid" here. 

    def fit(self, X, Y):
        self.model.fit(X, Y)

        # Model fitting on remote machine
        set_train_set(model_id = self.model_id, secret_key = self.secret_key, features = X, labels = Y)
        
        json_response = send_train_model_request(model = self.model, secret_key=self.secret_key, model_id=self.model_id)
        go_through_checklist(json_response)


    def predict(self, X):
        if len(np.array(X).shape) > 1:
            raise ValueError("Unforunately, Cube currently doesn't support multiple predictions at once. Please explictly wrap your iterable in a for-loop.")

        prediction = make_prediction(secret_key=self.secret_key, model_id=self.model_id, input_vector=X, pipeline=self)

        return prediction

    @staticmethod
    def load_model(model_id):
        # return 
        pass


def go_through_checklist(response_json):
    global exception_instances, exception_thresholds, VERBOSE

    # Check if there's any exceptions that we should raise
    probabilities = response_json["prediction_checklist_probabilities"]
    prediction_id = response_json["prediction_id"]

    exceptions_to_raise = []

    for checklist_item, probability in probabilities.items():

        # Add this exception to the exception list, if it isn't already being listened for
        Exception.make_exception(checklist_item)
        
        exception = exception_instances[checklist_item]
        
        # TODO: If probability is 0, nothing is raised. Should we do something costemically here?
        if probability > 0.9:

            if VERBOSE:
                print "[Cube] Logging Exception Request"
            
            url = BASE_URL + "/model/log_exception_raised"
            r = requests.post(url, 
                data={
                    "exception_name": checklist_item,
                    "secret_key": secret_key,
                    "model_id": model_id,
                    "prediction_id": prediction_id
                })

            if VERBOSE:
                print "[Cube] Recieved Response:\n----------------------\n", r.content, "\n------------------\n"

            raise exception_instances[checklist_item]



def make_prediction(secret_key, model_id, input_vector, pipeline, _local=True):
    url = BASE_URL + "/model/predict"
    r = requests.post(url, 
        data={
            "input_vector": cPickle.dumps(list(input_vector)),
            "secret_key": secret_key,
            "model_id": model_id,
        })

    response_json = process_response_json(r)
    go_through_checklist(response_json)

    # exceptions_to_raise = response_json["exceptions_to_raise"]
    prediction = response_json["prediction"]



    output = str(prediction)
    output = cPickle.loads(output)

    return output


def load_model(model_id, secret_key=None):
    url = BASE_URL + "/load"
    r = requests.get(url, params={"secret_key": secret_key})

    try:
        model_data = process_response_json(r)['model_data']
        if model_data is None:
            raise ValueError("There isn't a model here yet!")
        model = cPickle.loads(str(model_data))
    except:
        ValueError("Error loading model! Perhaps it doesn't exist yet!")
        return

    return model

def create_model_if_not_exists(model=None, model_id=None, secret_key=None, verbose=0):
    url = BASE_URL + "/model"
    model_cpickle = cPickle.dumps(model)

    input_type = "numpy"
    # results = process_input_in_batches(url, model_cpickle, input_type, model_id=model_id, secret_key=secret_key, verbose=verbose)

    # TODO remove model_id once web UI shares a DB with infrastructure, since it'll allow us to lookup model_id from there
    r = requests.post(url, data={"model_cpickle": model_cpickle, "model_id": model_id, "secret_key": secret_key, "ignore_if_exists": True})
    json_response = process_response_json(r)

    return json_response

def send_train_model_request(model=None, secret_key=None, model_id=None):
    """
        This function sends a trained model to Cube.
    """

    model_cpickle = cPickle.dumps(model)

    url = BASE_URL + "/model"
    r = requests.put(url, data={"model_id": model_id, "secret_key":secret_key, "model_cpickle": model_cpickle})
    json_response = process_response_json(r)

    return json_response

def check_if_valid_model(secret_key = None):
    url = BASE_URL + "/model/check_if_valid"
    results = requests.post(url, data={"secret_key": secret_key})
    return process_response_json(results)

def set_train_set(model_id = None, secret_key = None, features = None, labels = None, verbose=0):
    url = BASE_URL + "/model/set_train_set/features"
    input_type = "numpy"
    results = process_input_in_batches(url, features, input_type, secret_key=secret_key, model_id=model_id, verbose=verbose)

    url = BASE_URL + "/model/set_train_set/labels"
    input_type = "numpy"
    results = process_input_in_batches(url, labels, input_type, secret_key=secret_key, model_id=model_id, verbose=verbose)

    return True
