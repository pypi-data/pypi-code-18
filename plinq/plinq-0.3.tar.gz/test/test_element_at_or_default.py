from test.test_base import TestBase


class TestElementAtOrDefault(TestBase):
    def test_invalid_parameters(self):
        """
        Tests that calling element_at_or_default() should not raise a IndexError, in case the parameter is not valid
        but return the provided default value instead
        """
        self.assertIsNone(self._linq.element_at_or_default(None))
        self.assertIsNone(self._linq.element_at_or_default({}, None))
        self.assertEqual(self._linq.element_at_or_default(666, -1), -1)
        self.assertEqual(self._linq.element_at_or_default(-1, 0), 0)

    def test_valid_parameters(self):
        """
        Tests that calling element_at_or_default() with the right parameter will not raise an IndexError
        Also tests the the operator returns the right item
        """
        exception_raised = False
        try:
            self.assertEqual(self._linq.element_at_or_default(0), 1)
            self.assertEqual(self._linq.element_at_or_default(1), 2)
            self.assertEqual(self._linq.element_at_or_default(4), 5)
        except TypeError:
            exception_raised = True
        self.assertFalse(exception_raised)
