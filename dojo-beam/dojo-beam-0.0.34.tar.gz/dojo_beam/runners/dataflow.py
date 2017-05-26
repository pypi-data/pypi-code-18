from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import random
import tempfile
import subprocess
import apache_beam as beam

from apache_beam.utils.pipeline_options import PipelineOptions, SetupOptions, \
    GoogleCloudOptions, StandardOptions, \
    WorkerOptions
from dojo.runners.job import JobRunner


class DataflowBeamRunner(JobRunner):

    def run(self, job, config):
        job.setup()
        project_id = config['cloud']['project']

        dataset_name = job.config['name'].replace('_', '-')
        job_id = '%s--%s-%s' % (project_id, dataset_name, random.randint(1, 1000))

        options = PipelineOptions()
        setup_options = options.view_as(SetupOptions)
        setup_options.save_main_session = True
        setup_options.setup_file = os.path.join(os.getcwd(), 'setup.py')

        options.view_as(StandardOptions).runner = str('DataflowRunner')

        if 'cloud' in job.config and 'dataflow' in job.config['cloud']:
            worker_options = options.view_as(WorkerOptions)
            for key, value in job.config['cloud']['dataflow'].items():
                setattr(worker_options, key, value)

        gc_options = options.view_as(GoogleCloudOptions)
        gc_options.project = project_id
        gc_options.job_name = job_id
        gc_options.staging_location = job.store.as_uri(job.output_path('staging'))
        gc_options.temp_location = job.store.as_uri(job.output_path('temp'))

        keyfile_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if keyfile_path and os.path.isfile(keyfile_path):
            subprocess.check_call(['gcloud', 'auth', 'activate-service-account', '--key-file', keyfile_path])
            gcloud_key = json.loads(f.read())
            p12_keyfile_path = keyfile_path + '.p12'
            with tempfile.NamedTemporaryFile() as f:
                f.write(gcloud_key['private_key'])
                f.flush()
                subprocess.check_call('openssl rsa -in %s | openssl pkcs12 -password pass:notasecret -export -nocerts -out %s' % (f.name, p12_keyfile_path), shell=True)
            gc_options.service_account_key_file = p12_keyfile_path
            with open(keyfile_path, 'r') as f:
                gc_options.service_account_name = gcloud_key['client_email']

        pipeline = beam.Pipeline(options=options)

        job.run(pipeline)
        result = pipeline.run()
        result.wait_until_finish()
        job.store.teardown()
