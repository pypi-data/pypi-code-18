import unittest

import numpy as np
import pandas as pd
import subprocess
from multiprocessing import Process
import requests
import time
import sys
import tempfile
import os

from skater.core.explanations import Interpretation
from skater.util import exceptions
from arg_parser import create_parser
from skater.model import InMemoryModel, DeployedModel


tempdir = tempfile.mkdtemp()


def r_input_formatter(data):
    return {"input": pd.DataFrame(data).to_json(orient='records')}

def r_output_formatter(response, key='probability'):
    return np.array(response.json()['probability'])

def test_r_deploy_model():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data"
    feature_name = ['Status of existing checking account', 'Duration in month', 'Credit history'
        , 'Purpose', 'Credit amount', 'Savings account.bonds', 'Employment years'
        , 'Installment rate in percentage of disposable income'
        , 'Personal status and sex', 'Other debtors.guarantors', 'Present residence since'
        , 'Property', 'Age in years', 'Other installment plans', 'Housing',
                    'Number of existing credits at this bank'
        , 'Job', 'Number of people being liable to provide maintenance for', 'Telephone', 'Foreign worker',
                    'Status']

    p = R_async()
    p.join()
    with open(os.path.join(tempdir, 'run_r')) as f:
        while 'Starting server to listen on port 8000' not in f.read():
            time.sleep(1)
            print f.read()
            print "waiting for server"

    f_n = [f.replace(' ', '.') for f in feature_name]
    input_data = pd.read_csv(url, sep=' ', names=f_n)
    selected_input_data = input_data[['Status.of.existing.checking.account', 'Duration.in.month', 'Credit.history',
                                      'Savings.account.bonds']]

    deployed_model_uri = "http://datsci.dev:8000/predict"
    dep_model = DeployedModel(deployed_model_uri,
                              r_input_formatter,
                              r_output_formatter,
                              examples=selected_input_data.head(5))

    feature_names = np.array(selected_input_data.columns)
    interpreter = Interpretation(training_data=selected_input_data.head(5),
                                 feature_names=feature_names)

    plots = interpreter.partial_dependence.plot_partial_dependence(interpreter.data_set.feature_ids,
                                                                   dep_model,
                                                                   with_variance=True,
                                                                   sampling_strategy='random-choice',
                                                                   n_jobs=4,
                                                                   grid_resolution=10,
                                                                   n_samples=500,
                                                                   sample=True)

    #p.kill()

def sys_run_R_model():
    logfile = open(os.path.join(tempdir, 'r_run'), 'w')
    process = subprocess.Popen(["Rscript", "util/deployme.R"], stdout=logfile)#, stdin=None, stdout=None, stderr=None)
    return process, logfile



def R_async():
    #p = Process(target=wrap(sys_run_R_model, 'run_r'))
    p = Process(target=sys_run_R_model)
    #p.daemon = True
    p.start()
    return p
    #return sys_run_R_model()

test_r_deploy_model()
