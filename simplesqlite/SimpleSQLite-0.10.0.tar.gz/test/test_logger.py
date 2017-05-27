# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import print_function
from __future__ import unicode_literals

import pytest

from simplesqlite import (
    set_logger,
    set_log_level,
)
from simplesqlite._logger import logger

"""
class Test_logger:

    def test_normal(self, capsys):
        set_logger(is_enable=False)
        logger.info("info")

        out, err = capsys.readouterr()

        assert err == "info\n"
"""
