# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import logging
from datetime import datetime

import scrapy
from requests.compat import urljoin
from scrapy.crawler import CrawlerProcess

from pypackt.settings import BOOKS_SECTION
from pypackt.settings import PROJECT_URL
from pypackt.utils import get_user_login_data
from pypackt.utils import set_config_option

logger = logging.getLogger(__name__)


class PyPacktSpider(scrapy.Spider):

    name = 'pypackt'
    base_url = 'https://www.packtpub.com'
    start_urls = [urljoin(base_url, 'packt/offers/free-learning')]
    book = {}

    def start_requests(self):
        """Logs in into user's account before claiming ebook."""
        login, password = get_user_login_data()
        form_data = {
            'email': login,
            'password': password,
            'op': 'Login',
            'form_id': 'packt_user_login_form',
        }
        yield scrapy.FormRequest(
            url=self.start_urls[0],
            formdata=form_data,
            callback=self.parse
        )

    def parse(self, response):
        """Parses response to extract ebook's title and URL."""
        self.book = {
            'title':
                response.css('.dotd-title h2::text').extract_first().strip(),
            'url': urljoin(
                self.base_url,
                response.css('.twelve-days-claim::attr(href)').extract_first()),
        }
        yield scrapy.Request(
            url=self.book['url'],
            callback=self.on_success,
            errback=self.on_fail
        )

    def on_success(self, response):
        logger.info(self.book['title'])
        print(self.book['title'])
        set_config_option(BOOKS_SECTION, 'last', self.book['title'])
        today = datetime.now().date().isoformat()
        set_config_option(BOOKS_SECTION, today, self.book['title'])

    def on_fail(self, response):
        print(
            'Something went wrong - please check if you can login manually '
            'at {}\nIf logging in manually works, '
            'please raise an issue at: {}'.format(self.base_url, PROJECT_URL)
        )


def run_spider():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_ENABLED': False,
    })
    process.crawl(PyPacktSpider)
    process.start()
