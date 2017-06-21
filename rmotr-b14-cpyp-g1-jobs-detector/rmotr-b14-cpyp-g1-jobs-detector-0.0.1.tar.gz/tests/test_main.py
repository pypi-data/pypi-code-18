from __future__ import print_function
# -*- coding: utf-8 -*-
import re
import os
import unittest
import sys
import traceback

import responses
from click.testing import CliRunner

from jobs_detector import settings
from jobs_detector.main import jobs_detector


class HackerNewsTestCase(unittest.TestCase):

    def setUp(self):
        self.post_id = '11814828'
        fixture_path = os.path.join(settings.BASE_DIR, 'tests',
                                    'fixtures', '{}.html'.format(self.post_id))
        with open(fixture_path) as f:
            content = f.read()
        responses.add(responses.GET,
                      re.compile(re.escape(settings.BASE_URL.format(self.post_id))),
                      body=content, status=200,
                      content_type='text/html')

    @responses.activate
    def test_hacker_news_default_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news', '-i', self.post_id]
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Remote: 174 (19%)',
            'Postgres: 81 (9%)',
            'Python: 143 (16%)',
            'Javascript: 118 (13%)',
            'React: 133 (15%)',
            'Pandas: 5 (0%)',
        ]
        # Print useful error messages
        if not isinstance(result.exc_info[1], SystemExit) or\
           result.exc_info[1].code != 0:
            print(result.output, file=sys.stderr)
            print(result.exc_info, file=sys.stderr)
            traceback.print_tb(result.exc_info[2])

        for msg in expected:
            try:
                self.assertTrue(msg in result.output)
            except AssertionError:
                # Output does not match, print output and expected output
                print('Program output:', file=sys.stderr)
                print('===============', file=sys.stderr)
                print(result.output, file=sys.stderr)
                print('\nExpected output', file=sys.stderr)
                print('===============', file=sys.stderr)
                for msg in expected:
                    print(msg, file=sys.stderr)
                raise AssertionError('Output does not match ')

    @responses.activate
    def test_hacker_news_custom_keywords(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django']
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Python: 143 (16%)',
            'Django: 36 (4%)',
        ]
        # Print useful error messages
        if not isinstance(result.exc_info[1], SystemExit) or\
           result.exc_info[1].code != 0:
            print(result.output, file=sys.stderr)
            print(result.exc_info, file=sys.stderr)
            traceback.print_tb(result.exc_info[2])

        for msg in expected:
            try:
                self.assertTrue(msg in result.output)
            except AssertionError:
                # Output does not match, print output and expected output
                print('Program output:', file=sys.stderr)
                print('===============', file=sys.stderr)
                print(result.output, file=sys.stderr)
                print('\nExpected output', file=sys.stderr)
                print('===============', file=sys.stderr)
                for msg in expected:
                    print(msg, file=sys.stderr)
                raise AssertionError('Output does not match ')

    @responses.activate
    def test_hacker_news_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Remote: 174 (19%)',
            'Postgres: 81 (9%)',
            'Python: 143 (16%)',
            'Javascript: 118 (13%)',
            'React: 133 (15%)',
            'Pandas: 5 (0%)',

            'Combinations:',
            'Python-Remote: 25 (2%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (3%)',
        ]
        # Print useful error messages
        if not isinstance(result.exc_info[1], SystemExit) or\
           result.exc_info[1].code != 0:
            print(result.output, file=sys.stderr)
            print(result.exc_info, file=sys.stderr)
            traceback.print_tb(result.exc_info[2])

        for msg in expected:
            try:
                self.assertTrue(msg in result.output)
            except AssertionError:
                # Output does not match, print output and expected output
                print('Program output:', file=sys.stderr)
                print('===============', file=sys.stderr)
                print(result.output, file=sys.stderr)
                print('\nExpected output', file=sys.stderr)
                print('===============', file=sys.stderr)
                for msg in expected:
                    print(msg, file=sys.stderr)
                raise AssertionError('Output does not match ')

    @responses.activate
    def test_hacker_news_keywords_and_combinations(self):
        runner = CliRunner()
        result = runner.invoke(
            jobs_detector,
            ['hacker_news',
             '-i', self.post_id,
             '-k', 'python,django',
             '-c', 'python-remote,python-django,django-remote']
        )
        expected = [
            'Total job posts: 883',

            'Keywords:',
            'Python: 143 (16%)',
            'Django: 36 (4%)',

            'Combinations:',
            'Python-Remote: 25 (2%)',
            'Django-Remote: 6 (0%)',
            'Python-Django: 35 (3%)',
        ]
        # Print useful error messages
        if not isinstance(result.exc_info[1], SystemExit) or\
           result.exc_info[1].code != 0:
            print(result.output, file=sys.stderr)
            print(result.exc_info, file=sys.stderr)
            traceback.print_tb(result.exc_info[2])

        for msg in expected:
            try:
                self.assertTrue(msg in result.output)
            except AssertionError:
                # Output does not match, print output and expected output
                print('Program output:', file=sys.stderr)
                print('===============', file=sys.stderr)
                print(result.output, file=sys.stderr)
                print('\nExpected output', file=sys.stderr)
                print('===============', file=sys.stderr)
                for msg in expected:
                    print(msg, file=sys.stderr)
                raise AssertionError('Output does not match ')
