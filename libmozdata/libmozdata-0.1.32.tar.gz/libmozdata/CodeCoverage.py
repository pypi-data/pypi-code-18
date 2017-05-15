# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


class CodeCoverage():
    BASE_URL = 'https://activedata.allizom.org'
    URL = BASE_URL + '/query'

    def post_with_retries(self, url, payload=None, params=None, headers=None):
        retries = Retry(total=16, backoff_factor=1, status_forcelist=[429])

        s = requests.Session()
        s.mount(self.BASE_URL, HTTPAdapter(max_retries=retries))

        return s.post(url, json=payload, params=params, headers=headers)

    def get_coverage_summary(self):
        payload = {
          'from': 'coverage-summary',
          'limit': 10,
          'groupby': ['build.date', 'build.revision12'],
        }

        r = self.post_with_retries(self.URL, payload=payload)

        print(r.json())

    def get_data(self):
        payload = {
            'from': 'coverage-summary',
            'select': [
                { 'aggregate': 'count' },
                { 'value': 'source.file.total_uncovered', 'aggregate':'sum' },
                { 'value': 'source.file.total_covered', 'aggregate':'sum' }
            ],
            #'where': {
            #    'and': [
            #        # { 'prefix': { 'source.file.name': 'chrome://' } },
            #        { 'eq': { 'build.revision12':'04474cc44e28' } },
            #        { 'missing': 'test.url' }
            #    ]
            #},
            'groupby': [
                {
                    'name': 'file',
                    'value': {
                        'left': [
                            'source.file.name',
                            {
                                'add': [
                                    1,
                                    {
                                        'find': { 'source.file.name': '/' },
                                        'start': 9,
                                        'default': { 'length':'source.file.name' }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            'limit':1000
        }

        r = self.post_with_retries(self.URL, payload=payload)

        print(r.json())

CodeCoverage().get_coverage_summary()
CodeCoverage().get_data()
