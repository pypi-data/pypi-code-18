from __future__ import absolute_import
import unittest

import weightanalyser.dataanalyser as dataanalyser
import weightanalyser.visualisation as visualisation


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


class TestMakePlot(unittest.TestCase):
    def test_make_plot(self):
        """docstring for test_make_plot"""
        dataset = generate_testdataset()
        parameters = dataanalyser.calc_parameters(dataset, 14)
        visualisation.make_plot(dataset)
