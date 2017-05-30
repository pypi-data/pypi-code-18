"""
Search for plagiarisms scrapping DDG.
"""

import abc
import sys
import time
import warnings

import nltk
from robobrowser import RoboBrowser


warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


class Browser(metaclass=abc.ABCMeta):
    """ Search engine """
    # pylint: disable=too-few-public-methods

    @abc.abstractproperty
    def max_length(self):
        """ Max length property """
        return 0

    @abc.abstractproperty
    def result_number(self):
        """ Result number property """
        return 0

    @abc.abstractproperty
    def expected_results(self):
        """ Result number property """
        return 0

    def tokenize(self, text):
        """
        Split text in chunks acceptable by the search engine's max length.
        """

        def rejoin_sentence(subsentence, max_length):
            """
            Split a sentence in chunks if its too long
            """
            rejoint = []
            for word in subsentence.split(' '):
                if sum(len(a) for a in rejoint) + len(word) <= max_length:
                    rejoint.append(word)
                else:
                    yield ' '.join(rejoint)
                    rejoint = []

        for sentence in nltk.sent_tokenize(text):
            if len(sentence) >= self.max_length:
                yield from rejoin_sentence(sentence, self.max_length)
            else:
                yield sentence


class DuckDuckGo(Browser):
    """ DuckDuckGo search engine """
    # pylint: disable=too-few-public-methods
    max_length = 500
    result_number = 30
    expected_results = 10

    @staticmethod
    def search(query_term):
        """
        Make the initial search
        """
        browser = RoboBrowser()
        browser.open('https://duckduckgo.com/html')
        form = browser.get_form(action="/html/")
        form['q'].value = '"{}"'.format(query_term)
        browser.submit_form(form)
        return browser

    def search_max(self, query_term):
        """
        Search engine reported enough results to consider this
        part a plagiarism.
        """
        page = 0
        browser = self.search(query_term)
        results = [r.attrs["href"] for r in browser.select(".result__url")]

        while (page * self.result_number) < self.expected_results:
            while True:
                try:
                    page += 1
                    forms = browser.get_forms()
                    if len(forms) < 3:
                        # Not "next" button found, this is the last page.
                        # And we still haven't reached max results.
                        return False, results
                    browser.submit_form(forms[-1])
                    results += [r.attrs["href"] for r in
                                browser.select(".result__url")]
                    break
                except:  # pylint: disable=bare-except
                    time.sleep(1)
        return True, results

    def plagiarism_score(self, text):
        """
        Return a score based on the percentaje of times we
        encounter a phrase in an excessive number of results plus
        a modifier based on the number of times the result urls have
        been the same.
        """
        total_results = []
        for phrase in self.tokenize(text):
            done = False
            while not done:
                try:
                    too_many_results, results = self.search_max(phrase)
                    done = True
                except:
                    time.sleep(1)
            repeated = len([a for a in results if a in total_results])
            if results:
                yield int(too_many_results) * ((repeated / len(results)) + 1)
            else:
                yield 0
            total_results += results

    def is_plagiarism(self, text):
        """
        Return if we consider a text a plagiarism

        That is in case:

        - Too many chunks returned a number of results that we consider
          excessive for original content
        - Some of them have been found in the same document
        """
        results = list(self.plagiarism_score(text))
        return (100 * sum(results)) / len(results)


def main(filename, engine=DuckDuckGo, acceptable=10):
    """ Basic call from CLI """
    return engine().is_plagiarism(open(filename, 'r').read())


def cli():
    """ CLI """
    print(main(sys.argv[1]))
