from __future__ import absolute_import
import unittest

import weightanalyser.dataanalyser as dataanalyser


def generate_testdataset():
    """docstring for generate_testdataset"""
    dataset = { "general" : { "start_date" : "01-09-2016" }, "datapoints" : [] }

    for i_datapoint in range(40):
        datapoint = {}
        datapoint.update( { "date" : dataanalyser.get_date_from_number(i_datapoint,
                                                                       dataset["general"]["start_date"]) })
        datapoint.update( { "weight" : 100 })
        datapoint.update( { "fat_perc" : 20 } )
        datapoint.update( { "fat_mass" : 20 } )
        datapoint.update( { "mus_perc" : 40 } )
        datapoint.update( { "mus_mass" : 40 } )

        dataset["datapoints"].append(datapoint)

    return dataset


class TestGenerateTestdataset(unittest.TestCase):
    def test_generate_testdataset(self):
        """docstring for test_generate_testdataset"""
        testdataset = generate_testdataset()
        self.assertEqual(testdataset["datapoints"][0]['date'], "01-09-2016")
        self.assertEqual(testdataset["datapoints"][0]["weight"], 100)
        self.assertEqual(testdataset["datapoints"][0]["fat_perc"], 20)
        self.assertEqual(testdataset["datapoints"][0]["fat_mass"], 20)
        self.assertEqual(testdataset["datapoints"][0]["mus_perc"], 40)
        self.assertEqual(testdataset["datapoints"][0]["mus_mass"], 40)


class TestCalcParameters(unittest.TestCase):
    def test_calc_parameters(self):
        """docstring for test_generate_testdataset"""
        testdataset = generate_testdataset()
        parameters = dataanalyser.calc_parameters(testdataset, 14)
        self.assertEqual(parameters["weights_parameters"][0], 0)
        self.assertEqual(parameters["weights_parameters"][1], 100)
        self.assertEqual(parameters["fat_masses_parameters"][0], 0)
        self.assertEqual(parameters["fat_masses_parameters"][1], 20)
        self.assertEqual(parameters["mus_masses_parameters"][0], 0)
        self.assertEqual(parameters["mus_masses_parameters"][1], 40)


class TestGetDateFromNumber(unittest.TestCase):
    def test_get_date_from_number(self):
        self.assertEqual(dataanalyser.get_date_from_number(5, "01-08-2016"), "06-08-2016")

class TestGetNumberFromDate(unittest.TestCase):
    def test_get_number_from_date(self):
        """docstring for test_get_number_from_date"""
        self.assertEqual(dataanalyser.get_number_from_date("06-08-2016", "01-08-2016"), 5)


class TestGetIndexOfPeriod(unittest.TestCase):
    def test_get_index_of_period(self):
        """docstring for test_get_index_of_period"""
        dataset = generate_testdataset()
        period = 14
        self.assertEqual(dataanalyser.get_index_of_period(dataset, 10), 28)
