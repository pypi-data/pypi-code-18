from clevertimapi.endpoint import Endpoint
from clevertimapi.session import Session
from clevertimapi.utils import list_wrapper
from clevertimapi.contact import PhoneNumber
import sys
if sys.version_info[:2] < (2, 7):
    import unittest2 as unittest
else:
    import unittest


class FakeEndpoint(Endpoint):
    def __init__(self, session, key=None, content=None, lazy_load=False):
        self.session = session
        self._key = key
        self._content = content

    @property
    def key(self):
        return self._key

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'FakeEndpoint(%s)' % (self._key,)


class TestListWrapperSimple(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')

        self.lstw = list_wrapper(content=['val1', 'val2', 'val3'])

    def test_simple_append(self):
        self.assertEqual(len(self.lstw), 3)
        self.lstw.append('val4')
        self.assertEqual(self.lstw, ['val1', 'val2', 'val3', 'val4'])
        self.assertTrue('val4' in self.lstw)
        self.assertEqual(len(self.lstw), 4)

    def test_simple_extend(self):
        self.lstw.extend(('val4', 'val5'))
        self.lstw.extend(['val6', 'val7'])
        self.assertEqual(self.lstw, ['val1', 'val2', 'val3', 'val4', 'val5', 'val6', 'val7'])
        self.assertEqual(len(self.lstw), 7)

    def test_simple_insert(self):
        self.lstw.insert(0, 'val0')
        self.lstw.insert(3, 'val33')
        self.assertEqual(self.lstw, ['val0', 'val1', 'val2', 'val33', 'val3'])
        self.assertEqual(len(self.lstw), 5)

    def test_simple_remove(self):
        self.lstw.remove('val2')
        self.assertEqual(self.lstw, ['val1', 'val3'])

    def test_simple_remove_invalid_value(self):
        with self.assertRaises(ValueError):
            self.lstw.remove('val4')

    def test_simple_del_item(self):
        del self.lstw[1]
        self.assertEqual(self.lstw, ['val1', 'val3'])

    def test_simple_del_invalid_index(self):
        with self.assertRaises(IndexError):
            del self.lstw[3]

    def test_simple_pop(self):
        ret = self.lstw.pop(0)
        self.assertEqual(ret, 'val1')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val3')
        ret = self.lstw.pop()
        self.assertEqual(ret, 'val2')
        with self.assertRaises(IndexError):
            self.lstw.pop()

    def test_simple_clear(self):
        self.lstw.clear()
        self.assertEqual(self.lstw, [])

    def test_simple_plus_equal(self):
        self.lstw += ['val11', 'val21', 'val31']
        self.assertEqual(self.lstw, ['val1', 'val2', 'val3', 'val11', 'val21', 'val31'])


class TestListWrapperEndpoint(unittest.TestCase):

    def setUp(self):
        self.session = Session('APIKEY')
        Session.register_endpoint(FakeEndpoint)

        self.lstwc = list_wrapper(content=[1, 2, 3], endpoint_type=FakeEndpoint, session=self.session)

    def tearDown(self):
        Session.deregister_endpoint(FakeEndpoint)

    def test_endpoint_type_append(self):
        self.assertEqual(len(self.lstwc), 3)
        self.lstwc.append(FakeEndpoint(self.session, key=9))
        self.assertEqual(self.lstwc, [
            FakeEndpoint(self.session, key=1),
            FakeEndpoint(self.session, key=2),
            FakeEndpoint(self.session, key=3),
            FakeEndpoint(self.session, key=9)
        ])
        self.assertTrue(FakeEndpoint(self.session, key=2) in self.lstwc)
        self.assertEqual(len(self.lstwc), 4)

    def test_endpoint_type_extend(self):
        self.lstwc.extend((FakeEndpoint(self.session, key=7), FakeEndpoint(self.session, key=8)))
        self.lstwc.extend([FakeEndpoint(self.session, key=9), FakeEndpoint(self.session, key=10)])
        self.assertEqual(self.lstwc, [
            FakeEndpoint(self.session, key=1),
            FakeEndpoint(self.session, key=2),
            FakeEndpoint(self.session, key=3),
            FakeEndpoint(self.session, key=7),
            FakeEndpoint(self.session, key=8),
            FakeEndpoint(self.session, key=9),
            FakeEndpoint(self.session, key=10),
        ])
        self.assertEqual(len(self.lstwc), 7)

    def test_endpoint_type_insert(self):
        self.lstwc.insert(0, FakeEndpoint(self.session, key=8))
        self.lstwc.insert(3, FakeEndpoint(self.session, key=10))
        self.assertEqual(self.lstwc, [
            FakeEndpoint(self.session, key=8),
            FakeEndpoint(self.session, key=1),
            FakeEndpoint(self.session, key=2),
            FakeEndpoint(self.session, key=10),
            FakeEndpoint(self.session, key=3),
        ])
        self.assertEqual(len(self.lstwc), 5)

    def test_endpoint_type_remove(self):
        self.lstwc.remove(FakeEndpoint(self.session, key=2))
        self.assertEqual(self.lstwc, [
            FakeEndpoint(self.session, key=1),
            FakeEndpoint(self.session, key=3)
        ])

    def test_endpoint_type_remove_invalid_value(self):
        with self.assertRaises(ValueError):
            self.lstwc.remove(FakeEndpoint(self.session, key=4))

    def test_endpoint_del_item(self):
        del self.lstwc[1]
        self.assertEqual(self.lstwc, [FakeEndpoint(self.session, key=1), FakeEndpoint(self.session, key=3)])

    def test_endpoint_del_invalid_index(self):
        with self.assertRaises(IndexError):
            del self.lstwc[3]

    def test_endpoint_type_pop(self):
        ret = self.lstwc.pop(0)
        self.assertEqual(ret, FakeEndpoint(self.session, key=1))
        ret = self.lstwc.pop()
        self.assertEqual(ret, FakeEndpoint(self.session, key=3))
        ret = self.lstwc.pop()
        self.assertEqual(ret, FakeEndpoint(self.session, key=2))
        with self.assertRaises(IndexError):
            self.lstwc.pop()

    def test_endpoint_type_clear(self):
        self.lstwc.clear()
        self.assertEqual(self.lstwc, [])

    def test_endpoint_plus_equal(self):
        self.lstwc += [FakeEndpoint(self.session, key=5), FakeEndpoint(self.session, key=6)]
        self.assertEqual(self.lstwc, [
            FakeEndpoint(self.session, key=1),
            FakeEndpoint(self.session, key=2),
            FakeEndpoint(self.session, key=3),
            FakeEndpoint(self.session, key=5),
            FakeEndpoint(self.session, key=6)
        ])


class TestListWrapperCustomType(unittest.TestCase):

    def setUp(self):
        self.session = Session('APIKEY')

        self.lstwc = list_wrapper(
            content=[
                {'no': '07979463627', 'type': 'Mobile'},
                {'no': '0208342343', 'type': 'Work'},
                {'no': '0207343434', 'type': 'Fax'}
            ],
            custom_type=PhoneNumber,
            session=self.session
        )

    def test_custom_type_append(self):
        self.assertEqual(len(self.lstwc), 3)
        self.lstwc.append(PhoneNumber(phone_number='111222333', phone_type='Home'))
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0208342343', phone_type='Work'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax'),
            PhoneNumber(phone_number='111222333', phone_type='Home')
        ])
        self.assertTrue(PhoneNumber(phone_number='0207343434', phone_type='Fax') in self.lstwc)
        self.assertEqual(len(self.lstwc), 4)

    def test_custom_type_extend(self):
        self.lstwc.extend((PhoneNumber(phone_number='555666777', phone_type='Mobile'), PhoneNumber(phone_number='888999111', phone_type='Work')))
        self.lstwc.extend([PhoneNumber(phone_number='222333444', phone_type='Fax'), PhoneNumber(phone_number='111555888', phone_type='Pager')])
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0208342343', phone_type='Work'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax'),
            PhoneNumber(phone_number='555666777', phone_type='Mobile'),
            PhoneNumber(phone_number='888999111', phone_type='Work'),
            PhoneNumber(phone_number='222333444', phone_type='Fax'),
            PhoneNumber(phone_number='111555888', phone_type='Pager'),
        ])
        self.assertEqual(len(self.lstwc), 7)

    def test_custom_type_insert(self):
        self.lstwc.insert(0, PhoneNumber(phone_number='555666777', phone_type='Mobile'))
        self.lstwc.insert(3, PhoneNumber(phone_number='888999111', phone_type='Work'))
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='555666777', phone_type='Mobile'),
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0208342343', phone_type='Work'),
            PhoneNumber(phone_number='888999111', phone_type='Work'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax'),
        ])
        self.assertEqual(len(self.lstwc), 5)

    def test_custom_type_remove(self):
        self.lstwc.remove(PhoneNumber(phone_number='0208342343', phone_type='Work'))
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax')
        ])

    def test_custom_type_remove_invalid_value(self):
        with self.assertRaises(ValueError):
            self.lstwc.remove(PhoneNumber(phone_number='444333555', phone_type='Fax'))

    def test_custom_type_del_item(self):
        del self.lstwc[1]
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax')
        ])

    def test_custom_type_del_invalid_index(self):
        with self.assertRaises(IndexError):
            del self.lstwc[3]

    def test_custom_type_pop(self):
        ret = self.lstwc.pop(0)
        self.assertEqual(ret, PhoneNumber(phone_number='07979463627', phone_type='Mobile'))
        ret = self.lstwc.pop()
        self.assertEqual(ret, PhoneNumber(phone_number='0207343434', phone_type='Fax'))
        ret = self.lstwc.pop()
        self.assertEqual(ret, PhoneNumber(phone_number='0208342343', phone_type='Work'))
        with self.assertRaises(IndexError):
            self.lstwc.pop()

    def test_custom_type_clear(self):
        self.lstwc.clear()
        self.assertEqual(self.lstwc, [])

    def test_custom_type_plus_equal(self):
        self.lstwc += [PhoneNumber(phone_number='111222333', phone_type='Home'), PhoneNumber(phone_number='777888999', phone_type='Work')]
        self.assertEqual(self.lstwc, [
            PhoneNumber(phone_number='07979463627', phone_type='Mobile'),
            PhoneNumber(phone_number='0208342343', phone_type='Work'),
            PhoneNumber(phone_number='0207343434', phone_type='Fax'),
            PhoneNumber(phone_number='111222333', phone_type='Home'),
            PhoneNumber(phone_number='777888999', phone_type='Work')
        ])


class TestUtilsReadOnly(unittest.TestCase):
    def setUp(self):
        self.session = Session('APIKEY')
        Session.register_endpoint(FakeEndpoint)

        self.lstw = list_wrapper(content=['val1', 'val2', 'val3'], readonly=True)
        self.lstwc = list_wrapper(content=[1, 2, 3], endpoint_type=FakeEndpoint, session=self.session, readonly=True)
        self.lstwc2 = list_wrapper(
            content=[
                {'no': '07979463627', 'type': 'Mobile'},
                {'no': '0208342343', 'type': 'Work'},
                {'no': '0207343434', 'type': 'Fax'}
            ],
            custom_type=PhoneNumber,
            session=self.session,
            readonly=True
        )

    def test_append_fails(self):
        self.assertEqual(len(self.lstw), 3)
        with self.assertRaises(AssertionError):
            self.lstw.append('val4')
        with self.assertRaises(AssertionError):
            self.lstwc.append(FakeEndpoint(self.session, key=9))
        with self.assertRaises(AssertionError):
            self.lstwc2.append(PhoneNumber(phone_number='111222333', phone_type='Home'))
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)

    def test_extend_fails(self):
        with self.assertRaises(AssertionError):
            self.lstw.extend(('val4', 'val5'))
        with self.assertRaises(AssertionError):
            self.lstwc.extend((FakeEndpoint(self.session, key=9), FakeEndpoint(self.session, key=10)))
        with self.assertRaises(AssertionError):
            self.lstwc2.extend((PhoneNumber(phone_number='111222333', phone_type='Home'),))
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)

    def test_insert_fails(self):
        with self.assertRaises(AssertionError):
            self.lstw.insert(0, 'val0')
        with self.assertRaises(AssertionError):
            self.lstwc.insert(0, FakeEndpoint(self.session, key=9))
        with self.assertRaises(AssertionError):
            self.lstwc2.insert(0, PhoneNumber(phone_number='111222333', phone_type='Home'))
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)

    def test_remove_fails(self):
        with self.assertRaises(AssertionError):
            self.lstw.remove('val2')
        with self.assertRaises(AssertionError):
            self.lstwc.remove(FakeEndpoint(self.session, key=1))
        with self.assertRaises(AssertionError):
            self.lstwc2.remove(PhoneNumber(phone_number='07979463627', phone_type='Mobile'))
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)

    def test_del_fails(self):
        with self.assertRaises(AssertionError):
            del self.lstw[1]

    def test_pop_fails(self):
        with self.assertRaises(AssertionError):
            self.lstw.pop()
        with self.assertRaises(AssertionError):
            self.lstwc.pop()
        with self.assertRaises(AssertionError):
            self.lstwc2.pop()
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)

    def test_clear_fails(self):
        with self.assertRaises(AssertionError):
            self.lstw.clear()
        with self.assertRaises(AssertionError):
            self.lstwc.clear()
        with self.assertRaises(AssertionError):
            self.lstwc2.clear()
        self.assertEqual(len(self.lstw), 3)
        self.assertEqual(len(self.lstwc), 3)
        self.assertEqual(len(self.lstwc2), 3)
