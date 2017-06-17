"""
  File_downloader module
"""
# pylint: skip-file
from distutils.core import Command

class PyReqs(Command):
    description = "requirements.txt in 'setup' format"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        assert os.getcwd() == self.cwd, 'Must be in package root: %s' % self.cwd
        reqs = list()
        with open('requirements.txt', 'r') as f:
            reqs = re.split("\n", f.read())

        print("----Dependencies----\n")
        pprint.pprint(reqs)


class PyPrintPath(Command):
    description = "requirements.txt in 'setup' format"
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):        
        print("Install path: %s"% os.getcwd)
        
if __name__ == "__main__":
    print "File_downloader module"
