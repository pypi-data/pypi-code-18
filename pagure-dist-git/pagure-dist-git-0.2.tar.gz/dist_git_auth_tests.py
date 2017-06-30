from __future__ import print_function

import tempfile
import os

import mock

# These are the tests from the pagure/ git repo.
# Run with PYTHONPATH=.:/path/to/pagure/checkout nosetests dist_git_auth_tests.py
import tests

import dist_git_auth

expected = """
repo test
  R   = @all
  RWC master = pingou
  RWC f9000 = pingou
  -    f[0-9][0-9] = @all
  -    epel[0-9] = @all
  -    epel[0-9][0-9] = @all
  -    el[0-9] = @all
  -    olpc[0-9] = @all
  RWC = pingou

repo requests/test
  RWC = pingou

repo test2
  R   = @all
  RWC master = pingou
  RWC f9000 = pingou
  -    f[0-9][0-9] = @all
  -    epel[0-9] = @all
  -    epel[0-9][0-9] = @all
  -    el[0-9] = @all
  -    olpc[0-9] = @all
  RWC = pingou

repo requests/test2
  RWC = pingou

repo somenamespace/test3
  R   = @all
  RWC master = pingou
  RWC f9000 = pingou
  -    f[0-9][0-9] = @all
  -    epel[0-9] = @all
  -    epel[0-9][0-9] = @all
  -    el[0-9] = @all
  -    olpc[0-9] = @all
  RWC = pingou

repo requests/somenamespace/test3
  RWC = pingou
"""


class DistGitoliteAuthTestCase(tests.Modeltests):

    maxDiff = None

    def setUp(self):
        super(DistGitoliteAuthTestCase, self).setUp()
        self.configfile = tempfile.mkstemp()[1]

    def tearDown(self):
        try:
            os.remove(self.configfile)
        except:
            print("Couldn't remove %r" % self.configfile)
            pass
        super(DistGitoliteAuthTestCase, self).tearDown()

    @mock.patch('dist_git_auth.get_supported_branches')
    def test_write_gitolite_acls(self, get_supported_branches):
        get_supported_branches.return_value = ['master', 'f9000']
        print("Initializing DB.")
        tests.create_projects(self.session)
        print("Generating %r" % self.configfile)
        dist_git_auth.DistGitoliteAuth.write_gitolite_acls(
            self.session, self.configfile)
        print("Checking the contents of %r" % self.configfile)
        with open(self.configfile, 'r') as f:
            contents = f.read()
        self.assertMultiLineEqual(contents.strip(), expected.strip())

    def test_get_supported_branches(self):
        expected = ['master', 'f26', 'f25', 'f24', 'el6']
        actual = dist_git_auth.get_supported_branches('rpms', 'nethack')
        self.assertEquals(set(actual), set(expected))
