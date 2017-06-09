import os.path
import re

import weightanalyser.datahandeling as datahandeling


def add_measurement(weightanalyser_path, measurement):
    """docstring for add_measurement"""
    path = weightanalyser_path + "dataset.js"
    if os.path.isfile(path):
        dataset = datahandeling.read_dataset(path)
        dataset["datapoints"].append(measurement)
    else:
        dataset = {
            "general": {"start_date": measurement["date"]},
            "datapoints": [measurement]}
    datahandeling.write_dataset(path, dataset)

    return dataset


def check_date_format(date_string):
    if re.search("^[0-2][0-9]\-[0-1][0-9]\-[2][0][1][6-9]$", date_string):
        return True
    else:
        return False


def check_mass_value_format(value_string):
    if re.search("^[0-1]?[0-9][0-9]\.?[0-9]?$", value_string):
        return True
    else:
        return False


def check_percent_value_format(value_string):
    if re.match("^[0-9]?[0-9]\.?[0-9]?$", value_string):
        return True
    else:
        return False
