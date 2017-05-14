from test.test_base import TestBase


class TestElementAt(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling element_at() should raise a IndexError, in case the parameter is not valid
        """
        with self.assertRaises(IndexError):
            self._linq.element_at(None)
        with self.assertRaises(IndexError):
            self._linq.element_at({})
        with self.assertRaises(IndexError):
            self._linq.element_at(666)
        with self.assertRaises(IndexError):
            self._linq.element_at(-1)

    def test_valid_parameters(self):
        """
        Tests that calling element_at() with the right parameter will not raise an IndexError
        Also tests the the operator returns the right item
        """
        self.assertEqual(self._linq.element_at(0), 1)
        self.assertEqual(self._linq.element_at(1), 2)
        self.assertEqual(self._linq.element_at(4), 5)
