from scipy import stats
from datetime import datetime
from datetime import timedelta


def get_date_from_number(number, start_date):
    """docstring for get_date_from_number"""
    date_format = "%d-%m-%Y"
    start_date_object = datetime.strptime(start_date, date_format)
    number_date_object = start_date_object + timedelta(days=number)

    return number_date_object.strftime(date_format)


def get_number_from_date(date, start_date):
    """docstring for get_number_from_date"""
    date_format = "%d-%m-%Y"
    time_difference = datetime.strptime(date, date_format) - \
                      datetime.strptime(start_date, date_format)

    return time_difference.days


def get_index_of_period(dataset, period):
    length_dataset = len(dataset["datapoints"])
    i = length_dataset - 1
    dataset_period = 0
    while dataset_period < period and i != 0:
        dataset_period = get_number_from_date(dataset["datapoints"][length_dataset - 1]["date"],
                                              dataset["datapoints"][i]["date"])
        i -= 1
    return i


def calc_parameters(dataset, period):
    """docstring for get_weightparameters"""
    datenumbers = []
    weights = []
    fat_masses = []
    mus_masses = []

    # only take the last time_period days for the linear regression
    last_date = dataset["datapoints"][len(dataset["datapoints"]) - 1]["date"]
    last_index = get_number_from_date(last_date, dataset["general"]["start_date"]) + 1
    start_index = get_index_of_period(dataset, period)

    for i_datapoint in range(start_index, len(dataset["datapoints"]) - 1):
        datenumbers.append(
            get_number_from_date(dataset["datapoints"][i_datapoint]["date"], dataset["general"]["start_date"]))
        weights.append(dataset["datapoints"][i_datapoint]["weight"])
        fat_masses.append(dataset["datapoints"][i_datapoint]["fat_mass"])
        mus_masses.append(dataset["datapoints"][i_datapoint]["mus_mass"])

    weights_parameters = stats.linregress(datenumbers, weights)
    fat_masses_parameters = stats.linregress(datenumbers, fat_masses)
    mus_masses_parameters = stats.linregress(datenumbers, mus_masses)

    return {"weights_parameters": weights_parameters,
            "fat_masses_parameters": fat_masses_parameters,
            "mus_masses_parameters": mus_masses_parameters,
            "start_index": start_index,
            "last_index": last_index}
