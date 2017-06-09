#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_envcheckr
----------------------------------

Tests for `envcheckr` module.
"""


import pytest
from envcheckr import envcheckr


def test_parse_lines():
    lines_a = envcheckr.parse_lines('tests/env')
    assert len(lines_a) == 3
    lines_b = envcheckr.parse_lines('tests/env.example')
    assert len(lines_b) == 7


def test_parse_key():
    lines = envcheckr.parse_lines('tests/env')
    assert(envcheckr.parse_key(lines[0])) == 'FRUIT'
    assert(envcheckr.parse_key(lines[1])) == 'DRINK'
    assert(envcheckr.parse_key(lines[2])) == 'ANIMAL'


def test_get_missing_keys():
    file_a = 'tests/env'
    file_b = 'tests/env.example'
    missing_keys = envcheckr.get_missing_keys(file_a, file_b)
    assert(len(missing_keys)) == 4
    assert(missing_keys[0]) == 'FOOD=Pizza\n'
    assert(missing_keys[1]) == 'CODE=Python\n'
    assert(missing_keys[2]) == 'SPORT=Football\n'
    assert(missing_keys[3]) == 'CITY=Brisbane\n'
