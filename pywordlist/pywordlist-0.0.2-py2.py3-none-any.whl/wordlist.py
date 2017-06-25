import random
import requests


class WordList(object):
    def __init__(self, count, word_list='https://www.eff.org/files/2016/09/08/eff_short_wordlist_2_0.txt'):
        self.word_list = word_list
        self.count = count
        self.word_list = word_list

    def _get_wordlist(self):
        """
        Gets a word list and returns N random elements.
        This uses the eff list which is formatted as follows:
        "0001    word"
        """
        r = requests.get(self.word_list)
        return [random.choice([line.split()[1] for line in r.text.splitlines()]) for word in range(self.count)]

    def get_random_words(self):
        """
        Returns a list of words
        """
        return self._get_wordlist()
