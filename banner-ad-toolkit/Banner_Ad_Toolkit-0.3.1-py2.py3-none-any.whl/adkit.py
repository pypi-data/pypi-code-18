# -- coding: utf-8 --

# Copyright 2015 Tim Santor
#
# This file is part of proprietary software and use of this file
# is strictly prohibited without written consent.
#
# @author  Tim Santor  <tsantor@xstudios.agency>

"""Module doc string."""

# -----------------------------------------------------------------------------

# Prevent compatibility regressions
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

# Standard
import csv
import sys
import re
import os
import logging
import logging.handlers
import fnmatch

# 3rd Party
import six.moves.configparser as configparser

# -----------------------------------------------------------------------------


class AdKitBase(object):

    """Class doc string."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # config_file = os.path.expanduser('adkit.ini')
        # config = configparser.ConfigParser()
        # config.read(config_file)
        # # self.config = config
        # # self.set_dirs()

    def get_config(self):
        """Read and return our config."""
        config_file = os.path.expanduser('adkit.ini')
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def create_logger(self):
        """Create a logger."""
        self.logger.setLevel(logging.DEBUG)

        # Create logging format
        msg_fmt = '[%(levelname)s] [%(asctime)s] [%(name)s] %(message)s'
        date_fmt = '%Y-%m-%d %I:%M:%S %p'
        formatter = logging.Formatter(msg_fmt, date_fmt)

        # Create file handler
        fh = logging.handlers.RotatingFileHandler('adkit.log', backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # Create console handler
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        # ch.setFormatter(formatter)

        # Add logging handlers
        self.logger.addHandler(fh)

    def get_data(self, path):
        """Helper to return correct path to our non-python
        package data files."""
        root = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(root, 'templates', path)

    def get_list_from_csv(self, csv_file):
        """Open and read a CSV into a list using the column
        headers as key names."""
        try:
            fileref = open(csv_file, 'rU')
            csv_f = list(csv.DictReader(fileref))
            fileref.close()
            return csv_f
        except BaseException as err:
            sys.exit(err)

    def get_size_from_filename(self, filepath):
        """Return string such as 300x250."""
        basename = os.path.basename(filepath)

        pattern = re.compile(r'(\d{1,4}x\d{1,4})')
        match = pattern.search(basename)
        if match:
            return match.group()

        raise Exception('Unable to get size for: {0}'.format(basename))

    def get_size_from_dirname(self, dirpath):
        """Return string such as 300x250."""
        pattern = re.compile(r'(\d{1,4}x\d{1,4})')
        match = pattern.search(dirpath)
        if match:
            return match.group()

        raise Exception('Unable to get size for: {0}'.format(dirpath))

    def find_ad_dirs(self):
        """Find ad folders which include the naming convention: WIDTHxHEIGHT"""
        self.logger.info('Find folders matching pattern "WIDTHxHEIGHT"')
        pattern = re.compile(r'(\d{1,4}x\d{1,4})')
        matches = []
        for root, dirnames, filenames in os.walk(self.input_dir):
            for d in dirnames:
                if pattern.search(d):
                    dirpath = os.path.join(root, d)
                    matches.append(dirpath)

        return matches

    def get_files_matching(self, input_dir, match='*.png'):
        """Return all files of a type in the input dir no matter how deep."""
        self.logger.info('Get all files matching "%s"' % match)
        # logmsg.info('Get all files matching "%s"' % match, self.logger)
        matches = []
        for root, dirnames, filenames in os.walk(input_dir):
            for filename in fnmatch.filter(filenames, match):
                matches.append(os.path.join(root, filename))

        return matches

    def create_list(self, cds):
        """Create list from a comma delimited string."""
        current_list = cds.split(',')
        new_list = []
        for f in current_list:
            new_list.append(f.strip())
        return new_list
