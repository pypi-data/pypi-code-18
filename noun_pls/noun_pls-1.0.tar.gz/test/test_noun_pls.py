import unittest

from noun_pls.noun_pls import Nouns

class testNouns(unittest.TestCase):

    def setUp(self):
        self.Nouns = Nouns()

    def test_random_list(self):
        random_list = self.Nouns.random_list(10)
        self.assertEqual(len(set(random_list)), len(random_list))


if __name__ == '__main__':
    unittest.main()