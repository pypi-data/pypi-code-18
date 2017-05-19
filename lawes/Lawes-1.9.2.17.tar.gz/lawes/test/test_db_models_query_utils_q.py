
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
        query = Q(name='lawes')
        obj = Query(None)
        self.assertEqual(obj._as_sql(q_object=query), {'name': 'lawes'})
        query = query & Q(sex=1)
        obj._as_sql(q_object=query)
        query_expected = {'$and': [{'name': 'lawes'}, {'sex': 1}]}
        self.assertEqual(obj._as_sql(q_object=query), query_expected)
        query_other = Q(address='lawes street1') | Q(age__gt=2)
        obj._as_sql(q_object=query_other)
        query_other_expected = {'$or': [{'address': 'lawes street1'}, {'age': {'$gt': 2}}]}
        self.assertEqual(obj._as_sql(q_object=query_other), query_other_expected)
        query_combine = query & query_other
        self.assertEqual(obj._as_sql(q_object=query_combine), {'$and': [query_expected, query_other_expected]})
        query = Q(name_text__search='name')
        query = query | Q(address_text__search='address')
        query_result = {'$or': [{'name': {'$regex': 'n.*a.*m.*e', '$options': 'si'}}, {'address': {'$regex': 'a.*d.*d.*r.*e.*s.*s', '$options': 'si'}}]}
        self.assertEqual(obj._as_sql(q_object=query), query_result)

    # TODO all of them
