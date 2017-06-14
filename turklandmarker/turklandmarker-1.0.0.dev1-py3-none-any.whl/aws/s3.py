#! /usr/bin/env python
# -*- coding: utf-8 -*-
# S.D.G

"""Class to upload files to AWS S3 bucket"""

# Imports
import boto3
import os
from collections import defaultdict

__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = 'Monday 5 June  21:04:56 AEST 2017'
__license__ = 'BSD 3-Clause'


CONTENT_TYPES = {
    '.html': 'text/html',
    '.css' : 'text/css',
    '.jpg' : 'image/jpg',
    '.jpeg': 'image/jpeg',
    '.png' : 'image/png',
    '.svg' : 'image/svg+xml',
    '.js'  : 'application/javascript',
    '.json': 'application/json',
    '.eot' : 'application/vnd.ms-fontobject',
    '.woff' : 'application/font-woff',
    '.ttf' : 'application/x-font-ttf',
}

CONTENT_TYPES = defaultdict(lambda: 'text/plain',
                            CONTENT_TYPES)


class AWSS3(object):

    def __init__(self, config, debug_level=1):
        """Constructor"""

        self.debug_level = debug_level
        self.config = config 
        self.index_file = 'index.html'
        self.protocol_file = 'protocol.html'
        self.error_file = 'error.html'
        self.connected = False

        self.html_files = [
            self.index_file,
            self.protocol_file,
            self.error_file,
            ]

        self.index_link = "https://s3-%s.amazonaws.com/%s/%s" % (
            self.config['AWS-S3']['REGION'],
            self.config['AWS-S3']['BUCKET_NAME'],
            self.index_file)

    def connect(self):
        """Connect""" 
        self.s3 = boto3.client('s3',
            region_name=self.config['AWS-S3']['REGION'],
            aws_access_key_id=self.config['KEYS']['AWS-ID'],
            aws_secret_access_key=self.config['KEYS']['AWS-KEY'],
        )

        self.connected = True


    def generate_bucket_link(self):

        link = "https://s3-%s.amazonaws.com/%s/%s" % (
            self.config['AWS-S3']['REGION'],
            self.config['AWS-S3']['BUCKET_NAME'],
            self.index_file)
        if self.debug_level:
            print(link)

        return link 

    def create_bucket(self):
        """Create the bucket on AWS S3"""

        if not self.connected:
            self.connect()

        bucket_name = self.config['AWS-S3']['BUCKET_NAME']
        buckets = self.s3.list_buckets()['Buckets']

        exist_buckets = [bucket['Name'] for bucket in buckets]

        # The bucket already exists
        if bucket_name in exist_buckets:
            if self.debug_level:
                print("%s Bucket exists" % bucket_name)
            return buckets[exist_buckets.index(bucket_name)] 

        # Create the bucket
        return self.s3.create_bucket(
            ACL=self.config['AWS-S3']['ACL'],
            Bucket=bucket_name,
            CreateBucketConfiguration = {
                'LocationConstraint': self.config['AWS-S3']['REGION'],
            },
        )

    def upload_files(self):
        """Upload files to bucket""" 

        if not self.connected:
            self.connect()

        static_folder = self.config['LANDMARK-DETAILS']['STATIC_FOLDER']
        static_base = os.path.basename(static_folder)

        # Prepare the filenames and keys
        file_list = [
            (os.path.join(static_folder, filename), 
             os.path.join(static_base, os.path.basename(filename)))\
            for filename in os.listdir(static_folder)]

        # Add the files not included in the static folder
        file_list += [
            (filename, 
             os.path.basename(filename))\
            for filename in self.html_files]

        # Execute the upload
        for upload_name, upload_key in file_list:

            if self.debug_level:
                print("Uploading: %s" % upload_name)
            filename, ext = os.path.splitext(upload_name)
            if ext in CONTENT_TYPES:
                content_type = CONTENT_TYPES[ext]
            else:
                content_type = 'text/plain'
                if self.debug_level:
                    print("Unknown file extension")

            self.s3.upload_file(
                upload_name,
                self.config['AWS-S3']['BUCKET_NAME'],
                upload_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'ACL': self.config['AWS-S3']['ACL'],
                },
            ) 

