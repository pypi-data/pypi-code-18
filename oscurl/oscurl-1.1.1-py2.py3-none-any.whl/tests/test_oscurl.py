import testtools

from oscurl import oscurl


class OscurlTestCase(testtools.TestCase):

    def test_always_succeed(self):
        self.assertEqual(True, True)

    def test_check_version(self):
        self.assertTrue(oscurl.VERSION)
