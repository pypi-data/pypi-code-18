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

"""A set of `pytest` routines for the `.results` module.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest

import murdock.results


class TestDockingResult(object):

    @pytest.mark.parametrize(
        'quality_measure', murdock.results.QUALITY_MEASURES)
    @pytest.mark.parametrize(
        'test_input,expected', (
            (
                {
                    'tr': False,
                    'ts': False,
                    'qualities': (0.0, 2.0),
                    'scores': (1.0, 0.0),
                    'wsize': None
                }, [0.5, ]
            ),
            (
                {
                    'tr': True,
                    'ts': False,
                    'qualities': (0.0, 2.0),
                    'scores': (1.0, 0.0),
                    'wsize': None
                }, [1.0, ]
            ),
            (
                {
                    'tr': False,
                    'ts': True,
                    'qualities': (0.0, 2.0),
                    'scores': (1.0, 0.0),
                    'wsize': None
                }, [0.0, ]
            ),
        )
    )
    def test_get_rates(self, test_input, expected, quality_measure):
        d = murdock.results.DockingResult()
        d.receptor = murdock.results.MoleculeInfo()
        d.receptor.label = 'test_mol'
        step_ind = 0
        ulim = 1.
        for run_ind, (rdat, sdat) in enumerate(
                zip(test_input['qualities'], test_input['scores'])):
            run = murdock.results.DockingRunResult(d, ind=run_ind)
            step = run.new_step('test_title')
            step.status = 'finished'
            step.scoring = murdock.results.BasicScoringResult(step)
            step.scoring.total = sdat
            quality_data = {d.receptor: rdat}
            step.new_quality(quality_measure, quality_data)
            d.add_run(run)
        rates = d.get_rates(
            step_ind, quality_measure, ulim, top_ranked=test_input['tr'],
            top_scored=test_input['ts'], wsize=test_input['wsize'])
        assert rates == pytest.approx(expected)


class TestMultiQuality(object):

    @pytest.mark.parametrize(
        'quality_measure', murdock.results.QUALITY_MEASURES)
    @pytest.mark.parametrize(
        'test_input,expected', (
           (
                {
                    'tr': False,
                    'ts': False,
                    'qualities': (0.0, 0.5, 1.0, 1.5),
                    'scores': (3.0, 2.0, 1.0, 0.0)
                }, [0.75, 0.75, 0.75, 0.75]
            ),
            (
                {
                    'tr': True,
                    'ts': False,
                    'qualities': (0.0, 0.5, 1.0, 1.5),
                    'scores': (3.0, 2.0, 1.0, 0.0)
                }, [0.75, 1.0, 1.0, 1.0]
            ),
            (
                {
                    'tr': False,
                    'ts': True,
                    'qualities': (0.0, 0.5, 1.0, 1.5),
                    'scores': (3.0, 2.0, 1.0, 0.0)
                }, [0.75, 0.5, 0.25, 0.0]
            ),
        )
    )
    def test_get_rates(self, test_input, expected, quality_measure):
        d = murdock.results.DockingResult()
        d.receptor = murdock.results.MoleculeInfo()
        d.receptor.label = 'test_mol'
        step_ind = 0
        ulim = 1.
        for run_ind, (rdat, sdat) in enumerate(
                zip(test_input['qualities'], test_input['scores'])):
            run = murdock.results.DockingRunResult(d, ind=run_ind)
            step = run.new_step('test_title')
            step.status = 'finished'
            step.scoring = murdock.results.BasicScoringResult(step)
            step.scoring.total = sdat
            quality_data = {d.receptor: rdat}
            step.new_quality(quality_measure, quality_data)
            d.add_run(run)
        mq = d.steps[0].qualities[quality_measure]
        rates = mq.get_rates(
            ulim, top_ranked=test_input['tr'], top_scored=test_input['ts'])
        assert rates == pytest.approx(expected)




class TestTimingDict(object):

    TDICTS =  (
        murdock.results.TimingDict(**{'process': None, 'wall': None}),
        murdock.results.TimingDict(**{'process': 1.337, 'wall': None}),
        murdock.results.TimingDict(**{'process': None, 'wall': 13.37}),
        murdock.results.TimingDict(**{'process': 1.337, 'wall': 13.37})
        )

    @pytest.mark.parametrize(
        'test_input,expected', (
            (TDICTS[0], False),
            (TDICTS[1], False),
            (TDICTS[2], False),
            (TDICTS[3], True)
            ))
    def test_bool(self, test_input, expected):
        assert bool(test_input) is expected
