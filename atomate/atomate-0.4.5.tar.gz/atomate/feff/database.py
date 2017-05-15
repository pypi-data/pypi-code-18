# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines the database classes.
"""

from atomate.utils.database import CalcDb
from atomate.utils.utils import get_logger

__author__ = 'Kiran Mathew'
__credits__ = 'Anubhav Jain'
__email__ = 'kmathew@lbl.gov'

logger = get_logger(__name__)


class FeffCalcDb(CalcDb):

    def __init__(self, host="localhost", port=27017, database="feff", collection="tasks",
                 user=None, password=None):
        super(FeffCalcDb, self).__init__(host, port, database, collection, user, password)

    def build_indexes(self, indexes=None, background=True):
        # TODO: @matk86 - would suggest adding a couple of indexes -computron
        pass

    def reset(self):
        # TODO: @matk86 - shouldn't this be implemented? Seems simple? -computron
        pass
