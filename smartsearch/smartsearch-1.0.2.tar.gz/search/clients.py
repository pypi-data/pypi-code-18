# Builtin imports
import logging

#  Internal imports
from search import exceptions

# External imports
import wolframalpha
import google
import wikipedia
from newspaper import Article
import requests
from bs4 import BeautifulSoup


log = logging.getLogger()


class Client:
    """
    Basic query client
    """
    client_name = None
    key_required = False

    def __init__(self, key=None):
        """
        Instantiate a client

        :param key: The API key for the client
        """
        if self.key_required:
            if not key:
                raise exceptions.APIKeyRequiredError("Client {} must have an API key to run queries".format(self.client_name))
        self._key = key
        self._build_instance()

    def _build_instance(self):
        """
        Build the instance of the query
        """
        pass

    def query(self, query_text):
        """
        Send a query to the client

        :param query_text: The text of the query
        :return response: The response to the query
        """
        raise NotImplementedError("Client class should nto be called directly")


class Wolfram(Client):
    _client_instance = None
    key_required = True

    def _build_instance(self):
        """
        Instantiate wolframalpha.Client

        """
        print("Building instance with key {}".format(self._key))
        self._client_instance = wolframalpha.Client(self._key)

    def query(self, query_text):
        """
        Use the instantiated client to query
        """
        res = self._client_instance.query(query_text)
        try:
            next_result = res.results.__next__().text
            if next_result:
                return next_result
            else:
                return False
        except (StopIteration, AttributeError) as e:
            return False


class Google(Client):
    _key_required = False

    def query(self, query_text):
        # Query google
        search_object = google.search(query_text)
        # Determine if a wikipedia url is in the first 5 searches
        urls = []
        for i in range(0, 4):
            url = search_object.__next__()
            urls.append(url)
            # If it is, query with wikipedia
            if "wikipedia.org/wiki" in url:
                # Until I can find a better way to do this, I'm grabbing the title from the url, and querying that way
                article_title = url.split("wikipedia.org/wiki/")[1].replace("_", " ")
                log.debug("Found wikipedia article {0}".format(article_title))
                response = wikipedia.summary(article_title, sentences=2) + " ({0})".format(url)
                return response
        # If there were no wikipedia pages
        first_url = urls[0]
        try:
            article = Article(first_url)
            article.download()
            article.parse()
            article.nlp()
            article_summary = article.summary
            article_title = article.title
            return "{0}\n{1} - ({2})".format(
                article_summary, article_title, first_url
            )

        except Exception as article_exception:
            try:
                log.debug("Got error {0} while using newspaper, switching to bs4".format(
                    article_exception.args
                ))
                html = requests.get(first_url).text
                # Parse the html using bs4
                soup = BeautifulSoup(html, "html.parser")
                [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
                text = soup.getText()
                # break into lines and remove leading and trailing space on each
                lines = (line.strip() for line in text.splitlines())
                # break multi-headlines into a line each
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                # drop blank lines
                soup_text = '\n'.join(chunk for chunk in chunks if " " in chunk)
                response = format(soup_text) + " ({0})".format(first_url)
                return response
            except Exception as search_exception:
                log.error("Error {0} occurred while searching query {1}".format(
                   search_exception.args, query_text
                ))
                return False
