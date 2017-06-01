from unittest import TestCase
from restclients_core.util import urlencode, url_with_query


class TestURLUtils(TestCase):

    def test_url_with_query(self):
        params = {'student_id': 1033334, 'year': 2014, 'term_name': 'Autumn'}
        IAS_PREFIX = "/api/v1/evaluation"

        url = url_with_query(IAS_PREFIX, params)

        self.assertEqual(url, "/api/v1/evaluation?student_id=1033334"
                         "&term_name=Autumn&year=2014")

        params = {'student_id': 1033334, 'year': 2014, 'term_name': 'Autumn',
                  'alpha': 'omega'}

        url = url_with_query(IAS_PREFIX, params)

        self.assertEqual(url, "/api/v1/evaluation?alpha=omega&"
                         "student_id=1033334&term_name=Autumn&year=2014")

    def test_urlencode_dict(self):
        params = {'student_id': 1033334, 'year': 2014, 'term_name': 'Autumn'}
        url = urlencode(params)
        self.assertEqual(url, "student_id=1033334&term_name=Autumn&year=2014")

    def test_urlencode_tuple_list(self):
        params = [('student_id', 1033334), ('year', 2014),
                  ('term_name', 'Autumn')]

        url = urlencode(params)
        self.assertEqual(url, "student_id=1033334&term_name=Autumn&year=2014")
