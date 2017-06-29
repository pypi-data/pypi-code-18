# -*- coding: utf-8 -*-
# ######### COPYRIGHT #########
#
# Copyright(c) 2017
# -----------------
#
# * LabEx Archimède: http://labex-archimede.univ-amu.fr/
# * Laboratoire d'Informatique Fondamentale : http://www.lif.univ-mrs.fr/
# * Institut de Mathématiques de Marseille : http://www.i2m.univ-amu.fr/
# * Université d'Aix-Marseille : http://www.univ-amu.fr/
#
# This software is a port from LTFAT 2.1.0 :
# Copyright (C) 2005-2017 Peter L. Soendergaard <peter@sonderport.dk>.
#
# Contributors
# ------------
#
# * Denis Arrivault <contact.dev_AT_lif.univ-mrs.fr>
# * Florent Jaillet <contact.dev_AT_lif.univ-mrs.fr>
#
# Description
# -----------
#
# ltfatpy is a partial Python port of the Large Time/Frequency Analysis Toolbox
# (http://ltfat.sourceforge.net/), a MATLAB®/Octave toolbox for working with
# time-frequency analysis and synthesis.
#
# Version
# -------
#
# * ltfatpy version = 1.0.9
# * LTFAT version = 2.1.0
#
# Licence
# -------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ######### COPYRIGHT #########


"""Test of the plotdgtreal function

NOTE: Only the non-graphical features of plotdgtreal are tested here

.. moduleauthor:: Florent Jaillet
"""

from __future__ import print_function, division

import unittest
import numpy as np
from numpy.testing import assert_array_equal

from ltfatpy.gabor.plotdgtreal import plotdgtreal

# NOTE: The reference values used in the tests correspond to results
# obtained with Octave using ltfat 2.1.0


class TestPlotdgtreal(unittest.TestCase):

    # Called before the tests.
    def setUp(self):
        print('\nStart TestPlotdgtreal')

    # Called after the tests.
    def tearDown(self):
        print('Test done')

    def test_working(self):
        """Check that plotdgtreal is working as expected
        """
        out_ref = np.array([[0., 20.], [40., 60.], [80., 100.]])
        inputs = {}
        inputs['coef'] = np.array([[1., 10.], [100., 1000.],
                                  [10000., 100000.]])
        inputs['a'] = 1
        inputs['M'] = 1
        inputs['display'] = False
        out = plotdgtreal(**inputs)
        msg = ('wrong output in plotdgtreal with inputs ' + str(inputs))
        assert_array_equal(out_ref, out, msg)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlotdgtreal)
    unittest.TextTestRunner(verbosity=2).run(suite)
