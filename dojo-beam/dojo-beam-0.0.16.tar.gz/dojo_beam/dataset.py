from __future__ import absolute_import, print_function, unicode_literals

import os
import json
import tempfile
import apache_beam as beam

from dojo.dataset import Dataset

from .storage import BeamLocalFileStore, BeamGoogleStorageStore, BeamS3Store
from .transform import Conform, ConvertFrom, Validate
from .runners.direct import DirectBeamRunner
from .runners.dataflow import DataflowBeamRunner


class GoogleCloudAuth(object):

    def __init__(self, secrets):
        self.secrets = secrets

    def __enter__(self):
        if self.secrets is None:
            return
        self.f = tempfile.NamedTemporaryFile('w')
        json.dump(self.secrets, self.f)
        self.f.flush()
        self.previous_credentrials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.f.name

    def __exit__(self, *args):
        if self.secrets is None:
            return
        if self.previous_credentrials_file:
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.previous_credentrials_file
        else:
            del os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        self.f.close()


class BeamDataset(Dataset):

    RUNNERS = {
        'direct': DirectBeamRunner,
        'cloud': DataflowBeamRunner
    }

    STORES = {
        'file': BeamLocalFileStore,
        'gs': BeamGoogleStorageStore,
        's3': BeamS3Store
    }

    def run(self, pipeline):
        self.pipeline = pipeline
        with GoogleCloudAuth(self.secrets['store']['connection']):
            inputs = self.inputs()
            rows = self.process(inputs)
            self.output(rows)
            return rows

    def read_input(self, rows, dataset_name):
        schema = self.input_schema(dataset_name)
        return (rows | 'from_json ' + dataset_name >> beam.ParDo(ConvertFrom())
                     | 'validate ' + dataset_name >> beam.ParDo(Validate(schema)))

    def write_output(self, rows, format):
        # The storage class is expected to do the ConvertTo transform.
        return (rows | 'conform ' >> beam.ParDo(Conform(self.OUTPUT))
                     | 'validate ' >> beam.ParDo(Validate(self.OUTPUT)))
