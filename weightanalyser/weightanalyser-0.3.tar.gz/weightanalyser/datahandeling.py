import json


def read_dataset(path):
    f = open(path, "r")
    dataset = json.loads(f.read())
    f.close()
    return dataset


def write_dataset(path, dataset):
    f = open(path, "w")
    json.dump(dataset, f, indent=2)
    f.close()
