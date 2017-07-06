""" Helper class for working with 2D basecall type analyses.
"""
import numpy as np

from ont_fast5_api.analysis_tools.base_tool import BaseTool
from ont_fast5_api.fast5_file import Fast5File


class Basecall2DTools(BaseTool):
    """ Provides helper methods specific to 2D basecall analyses.
    """

    group_id = 'Basecall_2D'
    analysis_id = 'basecall_2d'

    def get_prior_alignment(self):
        """ Return the prior alignment that was used for 2D basecalling.

        :return: Alignment data table.
        """
        data_group = '{}/HairpinAlign'.format(self.group_name)
        data = self.handle.get_analysis_dataset(data_group, 'Alignment')
        return data

    def get_2d_call_alignment(self):
        """ Return the alignment and model_states from the 2D basecall.

        :return: Alignment data table.
        """
        data_group = '{}/BaseCalled_2D'.format(self.group_name)
        data = self.handle.get_analysis_dataset(data_group, 'Alignment')
        return data

    def add_prior_alignment(self, data):
        """ Add template or complement basecalled event data.
        
        :param data: Alignment table to be written.
        """
        path = 'Analyses/{}'.format(self.group_name)
        if 'HairpinAlign' not in self.handle.handle[path]:
            self.handle.add_analysis_subgroup(self.group_name, 'HairpinAlign')

        path = '{}/HairpinAlign'.format(self.group_name)
        self.handle.add_analysis_dataset(path, 'Alignment', data)

    def add_2d_call_alignment(self, data):
        """ Add the alignment and model_state data table..
        
        :param data: Alignment and model_state table to be written.
        """
        path = 'Analyses/{}'.format(self.group_name)
        if 'BaseCalled_2D' not in self.handle.handle[path]:
            self.handle.add_analysis_subgroup(self.group_name, 'BaseCalled_2D')

        path = '{}/BaseCalled_2D'.format(self.group_name)
        self.handle.add_analysis_dataset(path, 'Alignment', data)

    def get_called_sequence(self, fastq=False):
        """ Return the 2D sequence data, if present.

        :param fastq: If True, return a single, multiline fastq string. If
            False, return a tuple of (name, sequence, qstring).
        :return: Either the fastq string or the (name, sequence, qstring)
            tuple.
        :rtype: tuple or str
        """
        event_group = '{}/BaseCalled_2D'.format(self.group_name)
        data = self.handle.get_analysis_dataset(event_group, 'Fastq')
        if data is None:
            raise Exception('No 2D fastq data found.')
        if fastq:
            return data
        name, sequence, _, qstring = data.strip().split('\n')
        name = name[1:]
        return name, sequence, qstring

    def add_called_sequence(self, name, sequence, qstring):
        """ Add 2D basecalled sequence data.

        :param name: The record ID to use for the fastq.
        :param sequence: The called sequence.
        :param qstring: The quality string.
        """
        event_group = 'BaseCalled_2D'
        path = 'Analyses/{}'.format(self.group_name)
        if event_group not in self.handle.handle[path]:
            self.handle.add_analysis_subgroup(self.group_name, 'BaseCalled_2D')
        fastq_text = '@{}\n{}\n+\n{}\n'.format(name, sequence, qstring)
        fastq_arr = np.array(fastq_text, dtype=str)
        path = '{}/BaseCalled_2D'.format(self.group_name)
        self.handle.add_analysis_dataset(path, 'Fastq', fastq_arr)
