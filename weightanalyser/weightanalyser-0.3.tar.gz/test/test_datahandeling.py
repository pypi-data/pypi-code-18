from __future__ import absolute_import
import os
import unittest

import weightanalyser.datahandeling as datahandeling


class TestWriteread(unittest.TestCase):
    def test_writeread(self):
        """Test the wirte_datapoint and read_dataset functions of the datahandling module.

        It just writes a datapoint to a dataset in a file and reads the dataset afterwards.
        Because the datapoint is the only one in the dataset, the first index of the dataset
        should be equal to the datapoint.
        """
        datapoint = { "date" : "2016-09-13", "weight" : 90, "fat_perc" : 33, "mus_perc" : 33 }
        folder = "testdata"
        path = "testdata/test_writeread.dat"
        print os.getcwd()
        if not os.path.exists(folder):
            os.makedirs(folder)
        datahandeling.write_dataset(path, datapoint)
        dataset = datahandeling.read_dataset(path)
        self.assertEqual(datapoint, dataset)
