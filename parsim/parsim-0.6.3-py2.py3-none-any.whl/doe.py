# -------------------------------------------------------------------------
# Copyright (C) 2016-2017  RISE Research Institutes of Sweden AB
#
# This file is part of parsim.
#
# Main developer: Ola Widlund, RISE Research Institutes of Sweden AB
#                 (ola.widlund@ri.se, ola.widlund@yahoo.com)
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
# -------------------------------------------------------------------------
from __future__ import print_function
import textwrap
import sys
import numpy as np
import scipy as sp
import scipy.stats as stats

from parsim.loggers import logger
from parsim.core import ParsimError


schemes = ['mc', 'ff2n', 'lhs', 'pb']

def docstring_first_line(obj):
    return obj.__doc__.strip().splitlines()[0]

def help_message():
    """
    Create help message for DOE sampling, listing all available samplers in this module.

    Documentation is available from sampler classes docstrings.
    """
    sampler_descriptions = 'Available DOE sampling schemes:\n'
    thismodule = sys.modules[__name__]
    for sampler in schemes:
        f = getattr(thismodule, sampler)
        if f:
            sampler_descriptions += "    %-10s %s\n" % (sampler, docstring_first_line(f))

    description = '\n\n' + sampler_descriptions + '\n\n'
    description += textwrap.dedent('To get help on an individual sampling scheme, search '\
                                   'help for the doe command and add name of scheme. \nFor example:\n')
    description += '   psm help doe <scheme>\n'
    description += '     or\n'
    description += '   psm doe -h <scheme>\n'

    return description


class SamplingScheme(object):
    """Baseclass for sampling schemes, used for creating parsim Study cbjects."""

    sampling_method = None

    def __init__(self, distr_dict, **kwargs):
        assert isinstance(distr_dict, dict), 'Expected dict with distributions'
        self.args = kwargs
        self.data = {}
        self.norm_matrix = None
        self.value_matrix = None

        self.name = self.__class__.__name__
        self.description = docstring_first_line(self.__class__)
        self.parameters = kwargs.get('parameters', list(distr_dict.keys()))

        # Dicts for valid and required arguments
        self.valid_args = []
        self.required_args = []

        # Instantiate distributions from scipy.stats
        self.distr_dict = {}
        try:
            for p, d in distr_dict.items():
                self.distr_dict[p] = eval('stats.%s' % d)
        except:
            logger.error('Error creating distribution %s for parameter "%s"' % (d, p))
            raise

        # Common data
        self.set('nsamples', 0)
        self.set('npar', len(self.parameters))

        # Call sub-class _init(). May set default values.
        self._init()

        # Update data with all keyword arguments
        self.data.update(kwargs)

        # Check valid and required arguments (kwargs)
        self._check_args()

        # Run pre-calc stuff
        self._pre_calc()

        # Compute sampling matrices; normalized (norm_matrix) and actual values (value_matrix)
        self._calc_norm()
        if not self.get('nsamples'):
            self.set('nsamples', self.norm_matrix.shape[0])
        assert self.norm_matrix.shape == (self.get('nsamples'), self.get('npar')), 'Wrong dimension of norm_matrix!'

        self._calc_value()
        assert self.value_matrix.shape == (self.get('nsamples'), self.get('npar')), 'Wrong dimension of value_matrix!'

    def get(self, *key):
        if len(key)>1:
            return self.data.get(key[0], key[1])
        else:
            return self.data.get(key[0])

    def set(self, key, value):
        self.data[key] = value

    def add_valid_args(self, args):
        self.valid_args.extend(args)

    def add_required_args(self, args):
        self.required_args.extend(args)

    def _init(self):
        """
        Make scheme-specific initialization. Extended by subclasses.

        Example:

        # Add keyword information
        add_valid_args(['n', 'method'])
        add_required_args(['n'])
        """
        pass

    def _check_args(self):
        """Check validity of arguments."""
        unknown_args = set(self.args) - set(self.valid_args)
        missing_args = set(self.required_args) - set(self.args)

        if missing_args:
            logger.error('The following required DOE arguments are missing: %s'
                         % ', '.join(missing_args))
        if unknown_args:
            logger.warning('The following DOE arguments are unknown and ignored: %s'
                           % ', '.join(unknown_args))

    def _pre_calc(self):
        """Do preparations necessary before _calc is run."""
        pass

    def _calc_norm(self):
        """
        Process keyword arguments, then compute and set norm_matrix.

        Example for single reference case with distribution mean values:

        npar = self.get('npar')
        self.norm_matrix = np.zeros(1, npar)
        """
        raise NotImplementedError

    def _calc_value(self):
        """
        Compute value_matrix from norm_matrix.
        """
        raise NotImplementedError

    def write_caselist(self, filename):
        raise NotImplementedError

    def write_norm_matrix(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.norm_matrix)+'\n')

    def write_value_matrix(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self.value_matrix)+'\n')

    def get_case_definitions(self):
        """Output list of tuples (case_id, case_dict)"""
        n = self.get('nsamples')
        p = self.get('npar')
        cases = [(str(i+1), dict([(self.parameters[j], self.value_matrix[i, j]) for j in range(p)])) for i in range(n)]
        return cases

    def log_message(self):
        """Return log message for the sampling operation."""
        return 'Empty log message for sampling operation (baseclass)'

    @classmethod
    def help_message(cls):
        """
        Return help message for this sampler class, based on subclass docstring.

        Docstring should describe sampling method and all options.
        """
        return textwrap.dedent(cls.__doc__)


class RandomSamplingScheme(SamplingScheme):
    """Subclass for random sampling of distributions through their Cumulative Distribution Function (CDF)."""

    sampling_method = 'cdf'

    def _cdf_sampling(self):
        """Compute self.value_matrix, based on CDF of parameter distributions and random data in self.norm_matrix."""
        self.value_matrix = np.zeros_like(self.norm_matrix)
        for i in range(self.get('npar')):
            self.value_matrix[:, i] = self.distr_dict[self.parameters[i]].ppf(self.norm_matrix[:, i])

    def _init(self):
        super(RandomSamplingScheme, self)._init()
        self.add_valid_args(['seed'])
        self.set('seed', 1234)

    def _pre_calc(self):
        # Seed random number generator (numpy)
        seed = self.get('seed')
        assert isinstance(seed, int), 'Random seed must be integer'
        np.random.seed(seed)

    def _calc_value(self):
        """
        Create sampling matrix value_matrix, assuming subclass has already calculated norm_matrix.

        Overrides baseclass method. Normalized values (norm_matrix) are assumed to be in interval
        [0, 1] and actual values (value_matrix) are drawn from the inverse of the cumulative distribution
        function (CDF) of the parameter distributions.
        """
        self._cdf_sampling()

    def log_message(self):
        """Return log message for the sampling operation."""
        return 'Empty log message for CDF sampling operation (baseclass)'


class FactorLevelScheme(SamplingScheme):
    """Subclass for sampling factors at certain levels."""

    sampling_method = 'levels'

    def _init(self):
        super(FactorLevelScheme, self)._init()
        self.add_valid_args(['levels', 'alpha'])
        self.set('levels', 'int')
        self.set('alpha', 0.9545)

    def _level_sampling(self):
        """Compute self.value_matrix, based on factor levels in self.norm_matrix."""

        # Supported methods for selecting factor levels
        level_methods = ['int']
        assert self.get('levels') in level_methods, \
            'Expected "levels" to be one of the methods in %s' % repr(level_methods)

        self.value_matrix = np.zeros_like(self.norm_matrix)

        for i in range(self.get('npar')):
            if self.get('levels') == 'int':
                high, low = self.distr_dict[self.parameters[i]].interval(self.get('alpha'))
            else:
                raise NotImplementedError

            self.value_matrix[:, i] = (high + low) / 2. + (high - low) / 2. * self.norm_matrix[:, i]

    def _calc_value(self):
        """
        Create sampling matrix value_matrix, assuming subclass has already calculated norm_matrix.

        Overrides baseclass method. Normalized values (norm_matrix) are assumed to be in interval
        [0, 1] and actual values (value_matrix) are drawn from the inverse of the cumulative distribution
        function (CDF) of the parameter distributions.
        """
        self._level_sampling()

    def log_message(self):
        """Return log message for the sampling operation."""
        return 'Empty log message for factor-level sampling operation (baseclass)'


class mc(RandomSamplingScheme):
    """
    Monte Carlo random sampling.

    Keyword arguments:

        n      Number of samples (default: 10)
    """
    def _init(self):
        super(mc, self)._init()
        self.add_valid_args(['n'])

    def _calc_norm(self):
        # Default to 10 samples, if number not specified with argument 'n'
        self.set('nsamples', self.get('n', 10))

        # Compute random matrix
        self.norm_matrix = np.random.rand(self.get('nsamples'), self.get('npar'))


class lhs(RandomSamplingScheme):
    """
    Latin Hypercube sampling.

    Keyword arguments:

        n       Number (int) of sample points (default: one per parameter)
        mode    String that tells lhs how to sample the points:
                   'rand'                 Random within sampling interval (default),
                   'center', 'c'          Center within interval,
                   'maximin', 'm'         Maximize the minimum distance between points, but place
                                          the point in a randomized location within its interval,
                   'centermaximin', 'cm'  Same as 'maximin', but centered within the intervals,
                   'correlation', 'corr'  Minimize the maximum correlation coefficient.
        iter    Number of iterations (used by some modes; see pyDOE docs and code).
    """

    valid_modes = ['rand', 'center', 'c', 'maximin', 'm', 'centermaximin', 'cm', 'correlation', 'corr']

    def _init(self):
        super(lhs, self)._init()
        self.add_valid_args(['n', 'mode', 'iter'])
        self.set('n', self.get('npar'))
        self.set('mode', 'rand')
        self.set('iter', None)

    def _check_args(self):
        super(lhs, self)._check_args()
        mode = self.get('mode')
        if not mode in self.valid_modes:
            logger.error('Invalid mode (%s). Must be one of: %s' % (mode, self.valid_modes))

    def _calc_norm(self):
        import pyDOE as pd

        mode = self.get('mode')
        if mode == 'rand':
            mode = None

        # Compute random matrix
        self.norm_matrix = pd.lhs(self.get('npar'), samples=self.get('n'),
                                  criterion=mode, iterations=self.get('iter'))


class ff2n(FactorLevelScheme):
    """
    Two-level full factorial sampling.

    Keyword arguments:

        levels  Selection of method for mapping factor levels to actual values in the distribution.
                Alternatives:
                   'int'   (default) Use confidence interval with equal areas around the mean.
                           Width of interval is given by parameter 'alpha' (default: 0.9545)

        alpha   Width of confidence interval for 'int' method (see above). Default: 0.9545 (+/- 2*sigma)
    """

    def _calc_norm(self):
        import pyDOE as pd

        # Compute random matrix
        self.norm_matrix = pd.ff2n(self.get('npar'))


class pb(FactorLevelScheme):
    """
    Plackett-Burman (pbdesign).

    Another way to generate fractional-factorial designs is through the use of Plackett-Burman designs.
    These designs are unique in that the number of trial conditions (rows) expands by multiples of four
    (e.g. 4, 8, 12, etc.). The max number of factors allowed before a design increases the number of
    rows is always one less than the next higher multiple of four.

    Keyword arguments:

        levels  Selection of method for mapping factor levels to actual values in the distribution.
                Alternatives:
                   'int'   (default) Use confidence interval with equal areas around the mean.
                           Width of interval is given by parameter 'alpha' (default: 0.9545)

        alpha   Width of confidence interval for 'int' method (see above). Default: 0.9545 (+/- 2*sigma)
    """

    def _calc_norm(self):
        import pyDOE as pd

        # Compute random matrix
        self.norm_matrix = pd.pbdesign(self.get('npar'))
