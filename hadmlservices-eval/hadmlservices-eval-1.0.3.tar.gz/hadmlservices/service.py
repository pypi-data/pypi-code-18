import os
import sys
import urllib
from subprocess import call
import time
from hadmlservices import callbacks

AWS_REGION = "us-east-1"

def update(cb, key, message):
    print(message)
    cb.update_job(key, message)

def user_data(root_dir,
              prediction_s3,
              truth_s3,
              output_s3,
              params):
    
    prediction_dir = root_dir + '/prediction'
    truth_dir = root_dir + '/truth'
    output_dir = root_dir + '/output'

    cb = callbacks.CB();
    update(cb, "job_state", "creating input and output dirs")
    for x in [prediction_dir, truth_dir, output_dir]:
        if not os.path.exists(x):
            os.mkdir(x, 0777)
        os.chmod(x, 0777)    
    
    update(cb, "job_state", "downloading log agent")
    agent = root_dir + '/awslogs-agent-setup.py'
    url = ("https://s3.amazonaws.com/aws-cloudwatch/" +
           "downloads/latest/awslogs-agent-setup.py")
    f = urllib.URLopener()
    f.retrieve(url, agent)

    # work around for ubuntu 16.04
    update(cb, "job_state", "installing awslogs.service")
    path = os.path.dirname (os.path.abspath (__file__))
    call(["cp", path + "/awslogs.service", "/lib/systemd/system/awslogs.service"])
    os.chmod("/lib/systemd/system/awslogs.service", 0644)

    update(cb, "job_state", "launching log agent")
    os.chmod(agent, 0700)
    path = os.path.dirname (os.path.abspath (__file__))
    call([agent, "-n", "-r", AWS_REGION, "-c", path + "/awslogs.conf"])

    update(cb, "started", time.strftime('%Y-%m-%d %H:%M:%S'))    

    update(cb, "job_state", "copying prediction data")
    print("quiet copy: only errors are shown; please wait")
    call(["aws", "s3", "sync", "--only-show-errors", prediction_s3, prediction_dir])
    
    update(cb, "job_state", "copying truth data")
    print("quiet copy: only errors are shown; please wait")
    call(["aws", "s3", "sync", "--only-show-errors", truth_s3, truth_dir])

    update(cb, "job_state", "executing run_script")
    if params:
        call([root_dir + "/run_script",
              prediction_dir,
              truth_dir,
              output_dir,
              params])
    else:
        call([root_dir + "/run_script",
              prediction_dir,
              truth_dir,
              output_dir])

    update(cb, "job_state", "copying output data")
    print("quiet copy: only errors are shown; please wait")
    call(["aws", "s3", "sync", "--only-show-errors", "--acl", "bucket-owner-full-control",
           output_dir, output_s3])

    update(cb, "job_state", "finished")
    update(cb, "finished", time.strftime('%Y-%m-%d %H:%M:%S'))

    print("asynchronously terminating instance")
    cb.terminate_instance()
    return
