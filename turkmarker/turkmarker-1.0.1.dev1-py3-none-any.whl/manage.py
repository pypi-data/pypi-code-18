#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Python script to deploy site to AWS S3 and Mechanical Turk"""

# Imports
import os
import argparse
import shutil
from .utilities.base import parse_sys_config,\
    TEMPLATE_DATA
from .utilities.generate import GenerateSite
from .aws.s3 import AWSS3 
from .aws.mturk import AWSMTurk

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Wednesday 7 June  13:52:10 AEST 2017'
__license__ = 'BSD 3-Clause'


def get_options(argv=None):

    parser = argparse.ArgumentParser(
        description="turkmarker - Mechanical Turk Landmarking",
        epilog="See https://github.com/benjohnston24/MechTurkLandmarker"
        " for more information")

    parser.add_argument('-n', '--newproject', dest='new_project',
        help='Create new project with project name', required=False, type=str)
    parser.add_argument('-b', '--build', dest='build', action='store_true',
        help='Build the site', required=False)
    parser.add_argument('-u', '--upload', dest='upload', action='store_true',
        help='Upload files to S3', required=False)
    parser.add_argument('-m', '--mturk', dest='mturk', action='store_true',
        help='Create mechanical turk task', required=False)
    parser.add_argument('-r', '--results', dest='results', action='store_true',
        help='Get and store all available mechanical turk results', required=False)
    parser.add_argument('-c', '--config', type=str, dest='config_file',
        default='.configrc',
        help='Specify configuration file', required=False)
    parser.add_argument('-v', '--verbose', dest='debug_level', type=int,
        help='Verbocity 0: No debugging, 1: sys.stdout debugging', required=False, default=0)

    return parser.parse_args(argv)

def _main(args=None):

    args = get_options(args)

    if args.new_project:
        shutil.copytree(TEMPLATE_DATA, args.new_project)
        return

    config = parse_sys_config(args.config_file)
    # Create objects for later use
    s3 = AWSS3(config=config,
               debug_level=args.debug_level)
    mturk = AWSMTurk(config=config,
        debug_level=args.debug_level)

    # Build the site
    if args.build:
        site = GenerateSite(config)
        site.generate_lmrk_images(
            image_file=config['LANDMARK-DETAILS']['TEMPLATE_IMAGE'],
            landmarks_file=config['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS'],
            base_colour=config['LANDMARK-DETAILS']['BASE_COLOUR'],
            hi_colour=config['LANDMARK-DETAILS']['HI_COLOUR'],
            save_folder=config['LANDMARK-DETAILS']['STATIC_FOLDER'],
            radius=config['LANDMARK-DETAILS']['RADIUS'])
        site.generate_config_json()
        site.generate_javascript_check()

    # Upload files to S3
    if args.upload:
        s3.create_bucket()
        s3.upload_files()

    # Generate mechanical turk HIT
    if args.mturk:
        ext_question = mturk.create_external_question_XML(
            s3.generate_bucket_link())
        mturk.create_HIT(ext_question)

    # Get and store HIT results in files
    if args.results:
        hits = mturk.list_HITS()
        if args.debug_level:
            print("Getting HIT results")
        for hit in hits:
            mturk.save_results_to_file(hit[0])

if __name__ == "__main__":
    _main()
