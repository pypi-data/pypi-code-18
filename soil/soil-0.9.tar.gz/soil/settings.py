# General configuration
import yaml

output_folder = 'output'


def load(file='simulation.yml'):
    with open(file, 'r') as f:
        return list(yaml.load_all(f))
