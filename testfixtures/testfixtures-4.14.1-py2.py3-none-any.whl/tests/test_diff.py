# Copyright (c) 2008-2012 Simplistix Ltd
# See license.txt for license details.

from unittest import TestCase, TestSuite, makeSuite

from testfixtures import diff


class TestDiff(TestCase):

    def test_example(self):
        actual = diff('''
        line1
        line2
        line3
        ''',
                      '''
        line1
        line changed
        line3
        ''')
        expected = '''\
--- first
+++ second
@@ -1,5 +1,5 @@

         line1
-        line2
+        line changed
         line3
         '''
        self.assertEqual(
            [line.strip() for line in expected.split("\n")],
            [line.strip() for line in actual.split("\n")],
            '\n%r\n!=\n%r' % (expected, actual)
            )

    def test_no_newlines(self):
        actual = diff('x', 'y')
        # no rhyme or reason as to which of these comes back :-/
        try:
            expected = '@@ -1 +1 @@\n-x\n+y'
            self.assertEqual(
                expected,
                actual,
                '\n%r\n!=\n%r' % (expected, actual)
                )
        except AssertionError:  # pragma: no cover
            expected = '--- first\n+++ second\n@@ -1 +1 @@\n-x\n+y'
            self.assertEqual(
                expected,
                actual,
                '\n%r\n!=\n%r' % (expected, actual)
                )
