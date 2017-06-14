#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Common AWS API components"""

# Imports
import configparser
import os
import pkg_resources

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 5 June  21:04:56 AEST 2017'
__license__ = 'MPL v2.0'


# Default variables
TEMPLATE_DATA = pkg_resources.resource_filename('turkmarker', 'data/') 
DATA_FOLDER = os.getcwd()
DEFAULT_LMRKS_FILE = os.path.join(DATA_FOLDER, "template_landmarks.csv")
# Need to change this when creating turkmarker-admin
DEFAULT_SAVE_FOLDER = os.path.join(DATA_FOLDER, 'static')
# Need to move this
DEFAULT_RESULTS_FOLDER = os.path.join(DATA_FOLDER, 'results')
DEFAULT_SYS_CONFIG = os.path.join(DATA_FOLDER, '.configrc')

# Consider adding to default config file
AWS_ACCESS_KEY_ID = os.getenv('MECHTURK_ID') 
AWS_SECRET_ACCESS_KEY = os.getenv('MECHTURK_KEY') 


def parse_sys_config(config_file=DEFAULT_SYS_CONFIG, defaults=True):
    """Parse the config file
    
    Parameters:
    config_file: The path of the config file to read
    If is None, .configrc in the base directory is used

    defaults: Apply defaults to missing parameters. Defaults to True
    
    """

    if not os.path.exists(config_file):
        raise FileNotFoundError("Config file does not exist")

    config = configparser.ConfigParser()
    config.read(config_file)

    # Extract the info
    # Mandatory lines in configuration file
    data =  {
        'AWS-S3': 
        {
            'BUCKET_NAME': config['AWS-S3']['BucketName'],
            'REGION': config['AWS-S3']['Region'],
            'ACL': config['AWS-S3']['ACL'], 
        },
        'AWS-MTURK':
        {
            'END_POINT': config['AWS-MTURK']['EndPoint'],
            'REGION': config['AWS-MTURK']['Region'],
            'HIT_TITLE': config['AWS-MTURK']['HIT_Title'],
            'HIT_DESC': config['AWS-MTURK']['HIT_Description'],
            'HIT_KEYWORDS': config['AWS-MTURK']['HIT_Keywords'],
            'HIT_REWARD': config['AWS-MTURK']['HIT_Reward'],
            'HIT_MAXASSIGN': config['AWS-MTURK']['HIT_Max_Assignments'],
            'HIT_LIFE': config['AWS-MTURK']['HIT_LifetimeInSeconds'],
            'HIT_ASSIGNDUR': config['AWS-MTURK']['HIT_AssignmentDurationInSeconds'],
            'HIT_AUTOAPPROVEDELAY': config['AWS-MTURK']['HIT_AutoApprovalDelayInSeconds'],
            'HIT_FRAMEHEIGHT': config['AWS-MTURK']['HIT_Frame_Height'],
        },
        'KEYS':
        {
            'AWS-ID': AWS_ACCESS_KEY_ID,
            'AWS-KEY': AWS_SECRET_ACCESS_KEY, 
        },
        'LANDMARK-DETAILS':
        {
            'RADIUS': int(config['LANDMARK-DETAILS']['Radius']),
            'BASE_COLOUR': config['LANDMARK-DETAILS']['BaseColour'],
            'HI_COLOUR': config['LANDMARK-DETAILS']['HighlightColour'],
        },
    }

    # Optional items in configuration file
    if defaults:
        if 'TemplateImage' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['TEMPLATE_IMAGE'] =\
                os.path.join(DATA_FOLDER, "template_face.png")
        else:
            data['LANDMARK-DETAILS']['TEMPLATE_IMAGE'] =\
                config['LANDMARK-DETAILS']['TemplateImage']

        if 'TemplateLandmarks' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS'] =\
                os.path.join(DATA_FOLDER, "template_landmarks.csv")
        else:
            data['LANDMARK-DETAILS']['TEMPLATE_LANDMARKS'] =\
                config['LANDMARK-DETAILS']['TemplateLandmarks']

        if 'StaticFolder' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['STATIC_FOLDER'] =\
                DEFAULT_SAVE_FOLDER
        else:
            data['LANDMARK-DETAILS']['STATIC_FOLDER'] =\
                config['LANDMARK-DETAILS']['StaticFolder']

        if 'DisplayImage' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['DISPLAY_IMAGE'] =\
                os.path.join(DEFAULT_SAVE_FOLDER, "display_image.jpg")
        else:
            data['LANDMARK-DETAILS']['DISPLAY_IMAGE'] =\
                config['LANDMARK-DETAILS']['DisplayImage']

        if 'ResultsFolder' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['RESULTS_FOLDER'] =\
                DEFAULT_RESULTS_FOLDER
        else:
            data['LANDMARK-DETAILS']['RESULTS_FOLDER'] =\
                config['LANDMARK-DETAILS']['ResultsFolder']

        if 'ConfigJSON' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['CONFIG_JSON'] =\
                os.path.join(data['LANDMARK-DETAILS']['STATIC_FOLDER'],
                             'config.json')
        else:
            data['LANDMARK-DETAILS']['CONFIG_JSON'] =\
                config['LANDMARK-DETAILS']['ConfigJSON']

        if 'CheckJS' not in config['LANDMARK-DETAILS']:
            data['LANDMARK-DETAILS']['CHECK_JS'] =\
                os.path.join(data['LANDMARK-DETAILS']['STATIC_FOLDER'],
                             'check.js')
        else:
            data['LANDMARK-DETAILS']['CHECK_JS'] =\
                config['LANDMARK-DETAILS']['CheckJS']

    return data

