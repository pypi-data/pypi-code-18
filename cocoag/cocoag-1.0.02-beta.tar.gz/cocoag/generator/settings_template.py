import os
from pathlib import Path

# TODO: Move these to some kind of a common settings file
current_file_path = os.path.realpath(__file__)
GENERATOR_DIR_PATH = Path(current_file_path).parent
PACKAGE_ROOT_PATH = Path(GENERATOR_DIR_PATH).parent
S3_DIR_PATH = os.path.join(PACKAGE_ROOT_PATH, "s3")

# The location of the default config file the generator should use.
# You can change this to whatever you like. It defaults to the `coverage_gen_settings.py` file in this directory.
DEFAULT_CONFIG_FILE = os.path.join(GENERATOR_DIR_PATH, "coverage_settings_prod.json")
LOGGING_OUTPUT_FILE_DIR = "CHANGEME"
OUTPUT_FILE_NAME = "cocoag.svg"