import asyncio
import random
from urllib.parse import urlencode

from aiohttp.errors import ClientResponseError, ServerDisconnectedError
from bs4 import BeautifulSoup


# This is the maximum page size allowed.  Don't change this
page_size = 100
max_concurrent = 20
max_attempts = 10


# Generate url to search for papers
def _get_search_url(term):
    query = urlencode(dict(
        db='pubmed',
        term=term,
        usehistory='y'
    ))
    return ('https://eutils.ncbi.nlm.nih.gov/'
            'entrez/eutils/esearch.fcgi?{}').format(query)


# Generate url to fetch info about papers
def _get_fetch_url(webenv, query_key, paper_idx):
    query = urlencode(dict(
        db='pubmed',
        query_key=query_key,
        WebEnv=webenv,
        retmode='xml',
        retmax=str(page_size),
        retstart=str(paper_idx)
    ))
    return ('https://eutils.ncbi.nlm.nih.gov/'
            'entrez/eutils/efetch.fcgi?{}').format(query)


# Fetches results and yields them
class Fetcher(object):

    def __init__(self, session, term, max_papers=None):
        self.term = term
        self.session = session
        self.webenv = None
        self.query_key = None
        self.num_papers = None
        self.max_papers = max_papers

    # Total number of papers
    @property
    def total(self):
        return self.num_papers

    async def _get(self, url):
        # Don't try more than max_attempts times
        sleeptime = random.uniform(0, 1)
        for _ in range(max_attempts):
            try:
                async with self.session.get(url) as resp:
                    if resp.status == 200:
                        return await resp.text()
            except (ClientResponseError, ServerDisconnectedError,
                    RuntimeError, asyncio.TimeoutError):
                pass
            await asyncio.sleep(sleeptime)
            sleeptime = min(sleeptime * 2, 30)
        raise Exception("Too many failures")

    # Do initial search to get list of papers
    async def search(self):
        text = await self._get(_get_search_url(self.term))
        soup = BeautifulSoup(text, "lxml")

        self.webenv = soup.webenv.string
        self.query_key = soup.querykey.string
        self.num_papers = int(soup.count.string)

    @property
    def _num_papers_to_retrieve(self):
        return (
            self.num_papers
            if self.max_papers is None
            else min(self.max_papers, self.num_papers)
        )

    # Yield info about the papers
    def get_pages(self):
        # Urls to fetch papers |page_size| at a time
        # urls = [
        #     _get_fetch_url(self.webenv, self.query_key, paper_idx)
        #     for paper_idx in range(0, self._num_papers(), page_size)
        # ]
        # with open('foo.txt', 'a') as f:
        #     f.write(str(urls))
        return [
            self._get(_get_fetch_url(self.webenv, self.query_key, paper_idx))
            for paper_idx in range(0, self._num_papers_to_retrieve, page_size)
        ]
