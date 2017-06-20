# -*- coding: UTF-8 -*-
import logging
import requests

from time import sleep
from urllib.parse import quote_plus

from .parser import Parser
from .utilities import get_config


class BadConfigError(Exception):
    pass


class GoogleSpider():

    def __init__(self, query, country='us', proxy=None,
                 language='en-US', results_per_page=100,
                 max_results=10, wait_time=30,
                 ignore_https_warnings=False, localise=False,
                 start=0, min_date=None, max_date=None):

        # URL-encode query
        self.query = quote_plus(query)

        self.max_results = max_results
        self.country = country.lower()
        self.language = language
        self.localise = localise  # Override language with default country-language
        self.proxies = {}
        self.wait_time = wait_time
        self.results_per_page = results_per_page
        self.start = start
        self.min_date = min_date
        self.max_date = max_date
        self.tbs = []
        self.parser = Parser()

        self.config = get_config()

        # Set default language for localisation
        if self.localise:
            self.language = self.config['Language'].get(self.country)

        self.headers = {
            'User-Agent': self.config['DEFAULT'].get('user_agent'),
            'Accept': self.config['DEFAULT'].get('accept_header'),
            'Accept-Language': self.language,
            'Accept-Encoding': 'gzip, deflate',
        }

        # Set default get request parameters.
        self.params = {
            'q': self.query,
            'start': self.start,
            'num': self.results_per_page,
            'gws_rd': 'cr',
            'gl': self.country,
        }

        # Set custom date range parameters.
        if self.min_date:
            self.tbs.append('cd_min:{}'.format(self.min_date))

        if self.max_date:
            self.tbs.append('cd_max:{}'.format(self.max_date))

        if len(self.tbs) > 0:
            self.tbs.insert(0, 'cdr:1')
            self.params['tbs'] = ','.join(self.tbs)

        # Set proxies.
        if proxy is not None:
            self.proxies = {
                'http': proxy,
                'https': proxy
            }

        # Supress https warnings
        if ignore_https_warnings:
            from requests.packages.urllib3.exceptions import InsecureRequestWarning
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self.domain = self.config['Domain'].get(self.country)

        if not self.domain:
            raise ValueError('Country not supported - see config.ini.')

    def crawl(self):
        """
        Crawl Google results pages, return parsed results.
        """
        results = []
        url = 'https://www.{}/search'.format(self.domain)

        while len(results) < self.max_results:
            response = requests.get(url,
                                    params=self.params,
                                    headers=self.headers,
                                    proxies=self.proxies,
                                    verify=False)
            response.raise_for_status()
            items = self.parser.parse_results(response.text)

            # Finish if there no results.
            if len(items) == 0:
                logging.debug('No results')
                break
            else:
                results += items

            # Get next page link
            next_page = self.parser.parse_next_page_link(response.text)
            # Finish if there no more pages of results.
            if not next_page:
                logging.debug('No more results to fetch.')
                break

            url = 'https://www.{}{}'.format(self.domain, next_page)
            # Remove start parameter - we have next page URL.
            try:
                del self.params['start']
            except KeyError:
                pass

            # Set referer as previous page, more human-like.
            self.headers['referer'] = response.url

            # Finish if max results reached.
            if len(results) >= self.max_results:
                logging.debug('Reached max results.')
                break

            # Include a wait time if we
            # are not finished collecting data.
            logging.debug('Wating 30 seconds before next request.')
            sleep(self.wait_time)

        # Trim to max result size
        results = results[:self.max_results]

        return results
