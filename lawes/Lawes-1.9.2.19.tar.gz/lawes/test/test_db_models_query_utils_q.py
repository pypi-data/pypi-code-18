
import unittest
from lawes.test import Fruit
from lawes.db.models import Q
from lawes.db.models.sql import Query

class TestBdModelsQueryUtilsQ(unittest.TestCase):

    def setUp(self):
        self.clearall()

    def tearDown(self):
        self.clearall()

    def clearall(self):
        for test_obj in Fruit.objects.filter():
            test_obj.delete()

    def test_q(self):
        query = Q()
        result = Fruit.objects.filter(query)
        self.assertEqual(result.query.as_sql(), {})
        query = query & Q(name='lawes')
        result = Fruit.objects.filter(query)
        self.assertEqual(result.query.as_sql(), {'name': 'lawes'})
        query = query | Q()
        result = Fruit.objects.filter(query)
        self.assertEqual(result.query.as_sql(), {})
        query = query & Q(name='lawes') & Q(sex=1)
        result = Fruit.objects.filter(query)
        query_expected = {'$and': [{'name': 'lawes'}, {'sex': 1}]}
        self.assertEqual(result.query.as_sql(), query_expected)
        query_other = Q(address='lawes street1') | Q(age__gt=2)
        result = Fruit.objects.filter(query_other)
        query_other_expected = {'$or': [{'address': 'lawes street1'}, {'age': {'$gt': 2}}]}
        self.assertEqual(result.query.as_sql(), query_other_expected)
        query_combine = query & query_other
        result = Fruit.objects.filter(query_combine)
        self.assertEqual(result.query.as_sql(), {'$and': [query_expected, query_other_expected]})
        query = Q(name_text__search='name')
        query = query | Q(address_text__search='address')
        query_result = {'$or': [{'name': {'$regex': 'n.*a.*m.*e', '$options': 'si'}}, {'address': {'$regex': 'a.*d.*d.*r.*e.*s.*s', '$options': 'si'}}]}
        result = Fruit.objects.filter(query)
        self.assertEqual(result.query.as_sql(), query_result)

    # TODO all of them
