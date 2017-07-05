# Copyright (c) 2017 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for envars"""

from __future__ import print_function

import io
from six import StringIO

import os

import envars
import envars.envars as envars

def test_dictvalue():
    """py.test for dictvalue"""
    data = (
    (dict(a=1, b=2), "a", "default", 1), # dct, key, defvalue, expected
    (dict(a=1, b=2), "c", "default", "default"), # dct, key, defvalue, expected
    )
    for dct, key, defvalue, expected in data:
        result = envars.dictvalue(dct, key, defvalue)
        assert result == expected
        
def test_getenvars():
    """py.test for getenvars"""
    data = (
    ("""a=1
        b=2""", 'a', "default", "1"), # envtxt, key, defvalue, expected
    ("""a=1
        b=2""", 'c', "default", "default"), # envtxt, key, defvalue, expected
    )        
    for envtxt, key, defvalue, expected in data:
        fhandle = StringIO(envtxt)
        dct = envars.getenvars(fhandle=fhandle, defvalue=defvalue)
        result = dct[key]
        assert result == expected
    # test on os.environ -> as will happen on heroku
    os.environ['on_heroku'] = 'Yes'
    os.environ['another_heroku_value'] = 'avalue'
    dct = envars.getenvars(remoteKV=('on_heroku', 'Yes'))
    assert dct['another_heroku_value'] == 'avalue'
    # cleanup
    # os.environ.pop('on_heroku')
    # os.environ.pop('another_heroku_value')