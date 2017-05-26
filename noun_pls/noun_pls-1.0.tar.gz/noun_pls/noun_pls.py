"""

    A lightweight library that will give you a single noun or list nouns.

"""

import pkg_resources
import random

__author__ = 'John Liao <john@johnliao.org>'
__version__ = '1.0'


class Nouns:
    def __init__(self):
        self.nouns = []

        resource_package = __name__
        resource_path = '/'.join(('resources', 'nouns.txt'))

        nouns = pkg_resources.resource_string(resource_package, resource_path)

        for noun in nouns.split('\n'):
            self.nouns.append(noun)

    """
        Returns a random word.
    """
    def random_word(self):
        return random.choice(self.nouns)

    """
        Returns a unique list of given size of random words .
    """
    def random_list(self, n):
        assert n < len(self.nouns), 'You requested more words than exist in the library. Please use less than %s' % len(
            self.nouns)
        assert type(n) is int, 'Invalid number of nouns requested.'

        random_list = []

        while len(random_list) < n:
            w = random.choice(self.nouns)
            if w in random_list:
                continue
            random_list.append(w)

        return random_list