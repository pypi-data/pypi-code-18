import requests
from bs4 import BeautifulSoup as BS4Parser
import anidex.constants as constants
from requests.compat import urljoin
from datetime import datetime
import anidex.helpers as helpers


class Anidex(object):
    """docstring for Anidex"""

    def __init__(self, login=None, password=None):
        self.login = login
        self.password = password
        self.session = requests.Session()

    def is_connected(self):
        return self.login is not None or self.password is not None

    def parse_result(self, html_page):
        # Thanks Medusa
        torrents = []
        parser = BS4Parser(html_page, "html5lib")
        table_header = parser.find('thead')
        table_spans = table_header.find_all('span')
        labels = [label.get('title') for label in table_spans if
                  label.get('title') != 'Likes']
        rows = parser.find('tbody').find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            title = cells[labels.index('Filename')].span.get_text()
            download_url = cells[labels.index('Torrent')].a.get('href')
            download_url = urljoin(constants.ANIDEX_URL, download_url)
            seeders = cells[labels.index('Seeders')].get_text()
            leechers = cells[labels.index('Leechers')].get_text()
            torrent_size = cells[labels.index('File size')].get_text()
            size = helpers.parse_size(torrent_size)
            date = cells[labels.index('Age')].get('title')
            pubdate = datetime.strptime(date, "%Y-%m-%d %H:%M:%S %Z")
            magnet = helpers.execute_regex(constants.MAGNET_REGEX, str(row))
            likes = helpers.execute_regex(constants.LIKES_REGEX, str(row))
            item = {
                'title': title,
                'link': download_url,
                'magnet': magnet,
                'size': size,
                'seeders': seeders,
                'likes': likes,
                'leechers': leechers,
                'pubdate': pubdate,
            }
            torrents.append(item)
        return torrents

    def search(self, query=None, category=None, batch=True, raw=True,
               hentai=True, reencode=True, filter_mode=1, limit=500,
               lang_id='ALL'):

        payload = {}
        if type(batch) is not bool:
            raise Exception("Invalid batch value")
        if type(raw) is not bool:
            raise Exception("Invalid raw value")
        if type(hentai) is not bool:
            raise Exception("Invalid hentai value")
        if type(reencode) is not bool:
            raise Exception("Invalid reencode value")
        if helpers.check_filter_mode(filter_mode) is not True:
            raise Exception("Invalid filter_mode value")
        if helpers.check_lang_id(lang_id) is not True:
            raise Exception("Invalid lang_id value")
        if query is not None:
            payload['filename'] = query
        if category is not None:
            payload['category'] = category
        payload['batch'] = batch
        payload['raw'] = raw
        payload['hentai'] = hentai
        payload['reencode'] = reencode
        payload['filter_mode'] = filter_mode
        payload['page'] = 'torrents'
        payload['offset'] = 0
        payload['limit'] = limit
        payload['lang_id'] = helpers.translate_lang_id(lang_id)
        html_page = self.session.get(constants.SEARCH_URL, params=payload,
                                     headers=constants.HEADERS).text
        if 'No torrents.' in html_page:
            return None
        else:
            return self.parse_result(html_page)
