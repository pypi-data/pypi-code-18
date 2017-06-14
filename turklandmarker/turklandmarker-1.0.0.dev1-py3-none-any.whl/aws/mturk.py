#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Class to submit and monitor mechanical turk task"""

# Imports
import boto3
import os
import xmltodict
import json
import numpy as np
from collections import OrderedDict
from ast import literal_eval
from string import Template
from datetime import datetime
from turkmarker.utilities.generate import GenerateSite 

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Tuesday 6 June  16:29:28 AEST 2017'
__license__ = 'BSD 3-Clause'

EXTERNAL_Q_TEMPLATE = Template(
"""<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
      <ExternalURL>$url</ExternalURL>
      <FrameHeight>$frame_height</FrameHeight>
</ExternalQuestion>
""")

class AWSMTurk(object):

    def __init__(self, config, debug_level=1):
        """Constructor"""

        self.debug_level = debug_level
        self.config = config 
        self.connected = False

    def connect(self):
        """Connect""" 
        self.mturk = boto3.client('mturk',
            endpoint_url=self.config['AWS-MTURK']['END_POINT'],
            region_name=self.config['AWS-MTURK']['REGION'],
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
        )
        self.connected = True

    def create_HIT(self, question):
        """Create a HIT

        Parameters:
        question: The XML text of the question for the HIT as a string
        """

        if not self.connected:
            self.connect()

        new_hit = self.mturk.create_hit(
            Title=self.config['AWS-MTURK']['HIT_TITLE'],
            Description=self.config['AWS-MTURK']['HIT_DESC'],
            Keywords=self.config['AWS-MTURK']['HIT_KEYWORDS'],
            Reward=self.config['AWS-MTURK']['HIT_REWARD'],
            MaxAssignments=int(self.config['AWS-MTURK']['HIT_MAXASSIGN']),
            LifetimeInSeconds=int(self.config['AWS-MTURK']['HIT_LIFE']),
            AssignmentDurationInSeconds=int(self.config['AWS-MTURK']['HIT_ASSIGNDUR']),
            AutoApprovalDelayInSeconds=int(self.config['AWS-MTURK']['HIT_AUTOAPPROVEDELAY']),
            Question=question,
        )

        return new_hit

    def create_external_question_XML(self, url):
        """Construct the xml string for an external HIT question

        Parameters:
        url: the https url hosting the external question

        frame_height: the height of the external page in the HIT frame
        """

        self.external_question = EXTERNAL_Q_TEMPLATE.substitute(
            url=url, frame_height=self.config['AWS-MTURK']['HIT_FRAMEHEIGHT'])
        
        if self.debug_level:
            print(self.external_question)

        return self.external_question 

    def list_HITS(self):
        """List the currently submitted HITS"""

        if not self.connected:
            self.connect()

        hits = self.mturk.list_hits()
        hit_summary = []

        for hit in hits['HITs']:
            hit_summary.append((
                hit['HITId'],
                hit['Title'],
                hit['Description'],
                )
            )
        return hit_summary

    def get_results(self, hit_id, max_results=100,
        status=['Submitted', 'Approved', 'Rejected']):
        """Get the results for a particular HIT""" 

        if not self.connected:
            self.connect()

        results = self.mturk.list_assignments_for_hit(
            HITId=hit_id,
            MaxResults=max_results,
            AssignmentStatuses=status)

        return results

    def _manage_results_folder(self, hit_id):
        """Organise the results folder and return path"""

        results_folder = self.config['LANDMARK-DETAILS']['RESULTS_FOLDER']

        # If the folder doesnt exist, make it
        if not os.path.exists(results_folder):
            os.mkdir(results_folder)

        # Create a HIT specific folder in the results folder
        hit_results_folder = os.path.join(results_folder, hit_id)
        if not os.path.exists(hit_results_folder):
            os.mkdir(hit_results_folder)

        return hit_results_folder

    def _prepare_assignment_info(self, hit_id, hit_info, hit_results):
        """Prepare assignment information for saving"""

        hit_results_folder = self._manage_results_folder(hit_id)

        for hit_result in hit_results['Assignments']:
            result_dict = {}
            result_dict['Title'] = hit_info['Title']
            result_dict['Description'] = hit_info['Description']
            result_dict['CreationTime'] = str(hit_info['CreationTime'])
            result_dict['WorkerId'] = hit_result['WorkerId']
            result_dict['AssignmentId'] = hit_result['AssignmentId']
            result_dict['AssignmentStatus'] = hit_result['AssignmentStatus']
            result_dict['AcceptTime'] = str(hit_result['AcceptTime'])
            result_dict['Answer'] = hit_result['Answer'] 
            result_dict['Answers'] = [] 
            savename = "{}_{}".format(
                    datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),
                    hit_result['WorkerId'])
            save_folder = os.path.join(hit_results_folder,result_dict['AssignmentId'])

            if not os.path.exists(save_folder):
                os.mkdir(save_folder)
            savename = os.path.join(save_folder, savename)

            yield result_dict, savename

    def save_results_to_file(self, hit_id,
        max_results=100, 
        status=['Submitted', 'Approved', 'Rejected']):
        """Save the results to a file"""
        #TODO Look into pagination, 100 is max results that can be returned at a time

        if not self.connected:
            self.connect()

        hit_info = self.mturk.get_hit(HITId=hit_id)['HIT']
        hit_results = self.get_results(hit_id, max_results, status)

        marks = None
        for hit_result, savename in self._prepare_assignment_info(hit_id, hit_info, hit_results):
           # Parse Answer into
            xml_dict = xmltodict.parse(hit_result['Answer'])
            # There are multiple fields in the HIT layout
            for field in xml_dict['QuestionFormAnswers']['Answer']:
                hit_result['Answers'].append(field)
                if hasattr(field, 'keys'):
                    if 'marks' in field['QuestionIdentifier']:
                        marks = field['FreeText']
                        marks = literal_eval(marks)
                        vals = np.zeros((len(marks.keys()), 2))
                        for i in range(1, len(marks.keys()) + 1):
                            vals[i - 1,:] = marks['P%d' % i]
                        np.savetxt("%s.csv" % savename, vals, delimiter=',')

            del hit_result['Answer']
            with open("%s.json" % savename, 'w') as f:
                f.write(json.dumps(hit_result))
