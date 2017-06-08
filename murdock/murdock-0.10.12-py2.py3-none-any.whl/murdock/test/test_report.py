# -*- coding: utf-8 -*-
#
#   This file is part of the Murdock project.
#
#   Copyright 2016 Malte Lichtner
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""A set of `pytest` routines for `.report.report` module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.utils import viewitems

import collections

import pytest

import murdock.report.report


class TestTable(object):

    TEST_INPUT = (
                    (
                        ('row', 'no.', 1),
                        ('h1', 'sh1', 'r1f11'),
                        ('h1', 'sh2', 'r1f12'),
                    ),
                    (
                        ('row', 'no.', 2),
                        ('h1', 'sh2', 'r2f12'),
                    ),
                    (
                        ('row', 'no.', 3),
                        ('h2', 'sh1', 'r3f21'),
                    ),
                    (
                        ('row', 'no.', 4),
                        ('h2', 'sh2', 'r4f22'),
                        ('h2', 'sh1', 'r4f21'),
                    ),
                    (
                        ('h2', 'sh2', 'r5f22'),
                    ),
                    (
                        ('this empty column', 'is automatically removed', ''),
                    ),
                )

    @pytest.mark.parametrize('compact', (False, True))
    @pytest.mark.parametrize(
        'test_input,expected', (
            (
                TEST_INPUT,
                (
                    ('row',
                        (
                            ('no.', ['  1', '  2', '  3', '  4', '   ']),
                        )
                    ),
                    ('h1         ',
                        (
                            ('sh1  ', [
                                'r1f11', '     ', '     ', '     ', '     ']),
                            ('sh2  ', [
                                'r1f12', 'r2f12', '     ', '     ', '     ']),
                        )
                    ),
                    ('h2         ',
                        (
                            ('sh1  ', [
                                '     ', '     ', 'r3f21', 'r4f21', '     ']),
                            ('sh2  ', [
                                '     ', '     ', '     ', 'r4f22', 'r5f22']),
                        )
                    ),
                )
            ),
        )
    )
    def test_data(self, test_input, expected, compact):
        t = murdock.report.report.Table(compact=compact)
        for row_data in test_input:
            row = murdock.report.report.TableRow()
            for head, shead, field in row_data:
                row[head][shead] = field
            t.add_row(row)
        self._compare_data(t.data, expected, compact)

    @pytest.mark.parametrize(
        'test_input,expected', (
            (
                TEST_INPUT,
                (
                    (
                        ('row',
                            (
                                ('no.', ['  1', '  2']),
                            )
                        ),
                        ('h1         ',
                            (
                                ('sh1  ', ['r1f11', '     ']),
                                ('sh2  ', ['r1f12', 'r2f12']),
                            )
                        ),
                        ('h2         ',
                            (
                                ('sh1  ', ['     ', '     ']),
                                ('sh2  ', ['     ', '     ']),
                            )
                        ),
                    ),
                    (
                        ('row',
                            (
                                ('no.', ['  3', '  4', '   ']),
                            )
                        ),
                        ('h1         ',
                            (
                                ('sh1  ', ['     ', '     ', '     ']),
                                ('sh2  ', ['     ', '     ', '     ']),
                            )
                        ),
                        ('h2         ',
                            (
                                ('sh1  ', ['r3f21', 'r4f21', '     ']),
                                ('sh2  ', ['     ', 'r4f22', 'r5f22']),
                            )
                        ),
                    )
                )
            ),
        )
    )
    def test_split_h(self, test_input, expected):
        i_split = 2
        t = murdock.report.report.Table(compact=False)
        for row_data in test_input:
            row = murdock.report.report.TableRow()
            for head, shead, field in row_data:
                row[head][shead] = field
            t.add_row(row)
        for st, se in zip(t.split_h(i_split), expected):
            self._compare_data(st.data, se, compact=False)

    @pytest.mark.parametrize(
        'test_input,expected', (
            (
                TEST_INPUT,
                (
                    (
                        ('row',
                            (
                                ('no.', ['  1', '  2', '  3', '  4', '   ']),
                            )
                        ),
                        ('h1         ',
                            (
                                ('sh1  ', [
                                    'r1f11', '     ', '     ', '     ',
                                    '     ']),
                                ('sh2  ', [
                                    'r1f12', 'r2f12', '     ', '     ',
                                    '     ']),
                            )
                        ),

                    ),
                    (
                        ('row',
                            (
                                ('no.', ['  1', '  2', '  3', '  4', '   ']),
                            )
                        ),
                        ('h2         ',
                            (
                                ('sh1  ', [
                                    '     ', '     ', 'r3f21', 'r4f21',
                                    '     ']),
                                ('sh2  ', [
                                    '     ', '     ', '     ', 'r4f22',
                                    'r5f22']),
                            )
                        ),
                    )
                )
            ),
        )
    )
    def test_split_v(self, test_input, expected):
        head_split = 'h2'
        t = murdock.report.report.Table(compact=False)
        for row_data in test_input:
            row = murdock.report.report.TableRow()
            for head, shead, field in row_data:
                row[head][shead] = field
            t.add_row(row)
        for st, se in zip(t.split_v(head_split), expected):
            self._compare_data(st.data, se, compact=False)

    def _compare_data(self, data, expected, compact):
        assert len(data) == len(expected)
        for (k, v), (exp_k, exp_v) in zip(viewitems(data), expected):
            if compact:
                assert k == exp_k.strip()
            else:
                assert k == exp_k
            assert len(v) == len(exp_v)
            for (sk, sv), (exp_sk, exp_sv) in zip(viewitems(v), exp_v):
                if compact:
                    assert sk == exp_sk.strip()
                    assert tuple(sv) == tuple(_x.strip() for _x in exp_sv)
                else:
                    assert sk == exp_sk
                    assert tuple(sv) == tuple(exp_sv)
