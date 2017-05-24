from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division

from future.utils import raise_
from future.utils import raise_with_traceback
from future.utils import raise_from
from future.utils import iteritems

from builtins import FileExistsError
#The above future imports helps/ensures that the code is compatible
#with Python 2 and Python 3
#Read more at http://python-future.org/compatible_idioms.html

class PackageSkel(object):
    def hello(self):
        print('Hello world!')
