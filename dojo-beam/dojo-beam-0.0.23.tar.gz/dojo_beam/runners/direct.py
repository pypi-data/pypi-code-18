from __future__ import absolute_import, print_function, unicode_literals

import os
import random
import apache_beam as beam

from apache_beam.utils.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from dojo.runners.job import JobRunner


class DirectBeamRunner(JobRunner):

    def run(self, job, config):
        project_id = config['cloud']['project']

        dataset_name = job.config['name'].replace('_', '-')
        '%s--%s-%s' % (project_id, dataset_name, random.randint(1, 1000))

        options = PipelineOptions()
        setup_options = options.view_as(SetupOptions)
        setup_options.save_main_session = True
        setup_options.setup_file = os.path.join(os.getcwd(), 'setup.py')

        options.view_as(StandardOptions).runner = str('DirectRunner')

        pipeline = beam.Pipeline(options=options)

        job.setup()
        job.run(pipeline)
        job.teardown()

        result = pipeline.run()
        result.wait_until_finish()
