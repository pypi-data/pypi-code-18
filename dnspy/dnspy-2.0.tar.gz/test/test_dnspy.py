
import unittest

from dnspy.dnspy import Dnspy


class DnspyTestCase(unittest.TestCase):

    def setUp(self):
        self.dno = Dnspy('file:///tmp/mozilla_etlds.dat')
        #self.dno = Dnspy()

    def tearDown(self):
        pass

    def test_subdoms(self):
        expected = ['co.uk', 'google.co.uk', 'www.google.co.uk']
        result = self.dno.subdoms('1.2.3.www.google.co.uk')
        self.assertEqual(expected, result)

    def test_subdoms_n(self):
        expected = ['co.uk', 'google.co.uk', 'www.google.co.uk', '3.www.google.co.uk', '2.3.www.google.co.uk']
        result = self.dno.subdoms('1.2.3.www.google.co.uk', n=5)
        self.assertEqual(expected, result)

    def test_domlabels(self):
        expected = ['co.uk', 'google', 'www']
        result = self.dno.domlabels('1.2.3.www.google.co.uk')
        self.assertEqual(expected, result)

    def test_subdom_count(self):
        expected = ('google.co.uk', 4)
        result = self.dno.subdom_count('1.2.3.www.google.co.uk')
        self.assertEqual(expected, result)

    def test_idna_dom(self):
        expected = ['xn--h2brj9c', 'google.xn--h2brj9c']
        result = self.dno.subdoms('google.xn--h2brj9c')
        self.assertEqual(expected, result)

    def test_etld_only(self):
        expected = ['co.uk']
        result = self.dno.subdoms('co.uk')
        self.assertEqual(expected, result)
