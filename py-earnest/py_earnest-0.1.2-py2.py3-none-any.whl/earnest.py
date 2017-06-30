#!/usr/bin/env python
import numpy as np
import scipy.stats as sts
import statsmodels.tsa.stattools as stq

class HistoryPoint(object):
	def __init__(self, value):
		self._value = value

	def __len__(self):
		return 1

	@property
	def average(self):
		return self._value

	@property
	def _M2(self):
		return 0.0

	@property
	def _M3(self):
		return 0.0

	@property
	def _M4(self):
		return 0.0

class HistorySegment(object):
	""" Holds all relevant statistical quantities for a segment of the time series.

	No actual data points are stored, only the scaled moments (see article) are updated."""

	def __init__(self, numentries, average=0.0, M2=0.0, M3=0.0, M4=0.0, consumed=0):
		""" Prepares internal data structures.

		Parameters
		----------
		numentries : integer
			Maximum number of entries to be held in this segment."""
		self._numentries = numentries
		self._average = average
		self._M2 = M2
		self._M3 = M3
		self._M4 = M4
		self._consumed = consumed

	@property
	def capacity(self):
		return self._numentries

	@property
	def average(self):
		return self._average

	@property
	def variance(self):
		return self._M2 / float(len(self))

	@property
	def skewness(self):
		return np.sqrt(float(len(self))) * self._M3 / self._M2**(3./2.)

	@property
	def kurtosis(self):
		return float(len(self)) * self._M4 / self._M2**2

	def __len__(self):
		return self._consumed

	def __add__(self, other):
		""" Takes two history segments and creates a new one from them.

		Previous instances are not modified.

		Parameters
		----------
		other : HistorySegment
			Another instance to be added.

		Returns
		-------
		HistorySegment
			A new instance."""
		n_a = float(len(self))
		n_b = float(len(other))
		n = n_a + n_b
		delta = other.average - self.average
		s = (-n_b / n) * delta
		t = (n_a / n) * delta

		combined = HistorySegment(n)
		combined._consumed = n
		combined._average = self.average - s
		combined._M2 = self._M2 + other._M2 + n_a*s**2 + n_b*t**2
		combined._M3 = self._M3 + other._M3 + n_a*s**3 + n_b*t**3 + 3*(self._M2*s + other._M2*t)
		combined._M4 = self._M4 + other._M4 + n_a*s**4 + n_b*t**4 + 3*(self._M3*s + other._M3*t) + 6*(self._M2*s**2 + other._M2*t**2)

		return combined

class History(object):
	""" Holds a complete time series history and deals with all bookkeeping. """
	def __init__(self, levels):
		""" Prepares the object.

		Parameters
		----------
		levels : integer
			The number of history levels (in powers of two) to keep around."""
		if levels < 3:
			raise ValueError('At least a history of three segment sizes is required.')
		self._levels = levels
		self._current_level = 1

		self._segments = []

	def __len__(self):
		numvalues = len(self._segments) * self.segment_length
		if len(self._segments) > 0:
			numvalues += len(self._segments[-1]) - self.segment_length
		return numvalues		

	@property
	def segment_length(self):
		""" The length (in numbers of time series values) of the segments currently in use."""
		return 2**self._current_level

	@property
	def complete_blocks(self):
		""" The number of complete segments already in the history."""
		if len(self._segments) == 0:
			return 0
		if self._segments[-1].capacity == len(self._segments[-1]):
			return len(self._segments)
		else:
			return len(self._segments) - 1

	def _determine_offsets(self, nvalues):
		""" Calculates offsets of history segments in a given time series segment to be consumed.

		Parameters
		----------
		nvalues : integer
			Number of data points to be consumed.

		Returns
		-------
		current_segment : integer
			Number of the first data points to be used for completing the already started segment.
		complete_segments : integer
			Number of the second data points that span complete segments.
		partial_segment : integer
			Number of third remaining data points that do not complete a segment any more."""
		current_segment = 0
		if len(self._segments) > 0:
			current_segment = self._segments[-1].capacity - len(self._segments[-1])

		complete_segments = int(np.floor((nvalues - current_segment) / self.segment_length)) * self.segment_length

		partial_segment = nvalues - complete_segments - current_segment
		return current_segment, complete_segments, partial_segment

	@staticmethod
	def _should_level(numvalues, len_history):
		""" The level of detail to be used for a given number of data points and history length."""
		if len_history < 1:
			raise ValueError('At least one history level is required.')
		if numvalues == 0:
			return 1
		return max(1, int(np.ceil(np.log(numvalues)/np.log(2))) - len_history + 1)

	def _complete_current(self, values):
		""" Completes the last segment in the history.

		Parameters
		----------
		values : iterable
			Of exactly the matching length.

		Raises
		------
		ValueError
			If the number of values does not exactly complete the final segment.
		ValueError
			If an empty segment would be completed."""
		if len(values) == 0:
			return
		if len(self._segments) == 0:
			raise ValueError('Cannot complete an empty segment.')
		if len(values) + len(self._segments[-1]) != self._segments[-1].capacity:
			raise ValueError('Invalid count %d of time series values.' % len(values))

		for value in values:
			p = HistoryPoint(value)
			self._segments[-1] += p

	def _complete_segments(self, values):
		""" Adds complete segments to the history.

		Parameters
		----------
		values : iterable
			Of exactly integer multiple length of the current segment length.

		Raises
		------
		ValueError
			if the number of values does not match the current segment length."""
		if len(values) % self.segment_length != 0:
			raise ValueError('Invalid count %d of time series values.' % len(values))
		if len(values) == 0:
			return

		values = np.array(values).reshape((-1, self.segment_length))
		averages = np.average(values, axis=1)
		diff = values.T - averages
		diff_sq = diff * diff
		M2s = np.average(diff_sq, axis=0)
		M3s = np.average(diff * diff_sq, axis=0)
		M4s = np.average(diff_sq * diff_sq, axis=0)
		for segment in zip(averages, M2s, M3s, M4s):
			s = HistorySegment(self.segment_length, *segment, consumed=self.segment_length)
			self._segments.append(s)

	def _complete_partial(self, values):
		""" Adds values to the last partial segment of the history.

		Parameters
		----------
		values : iterable
			Shorter than a complete segment.

		Raises
		------
		ValueError
			if the number of values does not match the current segment length."""
		if len(values) >= self.segment_length:
			raise ValueError('Invalid count %d of time series values.' % len(values))
		if len(values) == 0:
			return

		s = HistorySegment(self.segment_length)
		for value in values:
			s += HistoryPoint(value)
		self._segments.append(s)

	@staticmethod
	def _split_even_odd(arr):
		if len(arr) % 2 == 1:
			return arr[:-1], arr[-1]
		else:
			return arr, None

	def _shift_level(self, target):
		if target < self._current_level:
			raise ValueError('Cannot decrease level.')

		for step in range(self._current_level, target):
			even_segments, odd_segment = History._split_even_odd(self._segments)

			new_segments = even_segments[::2] + even_segments[1::2]
			if odd_segment is not None:
				odd_segment._numentries *= 2
				self._segments = new_segments + [odd_segment]
			else:
				self._segments = new_segments

			self._current_level += 1

	def consume(self, values):
		""" Takes a stream of time series points and add them to the internal representation.

		No copy of the underlying time series is made.

		Parameters
		----------
		values : iterable
			The list of data points from the time series in the order they have been recorded."""
		nvalues = len(values)

		# Shift data to the correct power level
		should_level = History._should_level(len(self) + nvalues, self._levels)
		self._shift_level(should_level)

		# Consume data
		current_segment, complete_segments, partial_segment = self._determine_offsets(nvalues)
		self._complete_current(values[:current_segment])
		self._complete_segments(values[current_segment:current_segment + complete_segments])
		self._complete_partial(values[current_segment + complete_segments:])

	@property
	def active_levels(self):
		numvalues = len(self)
		minimum = History._should_level(numvalues, self._levels)
		maximum = int(np.ceil(np.log(numvalues)/np.log(2)))
		return range(minimum, maximum + 1)

	def build_cache(self):
		""" Creates a cache of coarse segment values derived from the greatest level of detail available."""
		self._cache = {}

		for idx, level in enumerate(self.active_levels):
			n_subsegments = 2**idx

			groups = [self._segments[i:i + n_subsegments] for i in xrange(0, len(self._segments), n_subsegments)]
			self._cache[level] = [sum(group[1:], group[0]) for group in groups if len(group) == n_subsegments]

		if len(self._segments) == 0:
			self._cache['total'] = None
		else:
			base = self._segments[0]
			for segment in self._segments[1:]:
				base += segment
			self._cache['total'] = base

	def clear_cache(self):
		del self._cache

	@property
	def cache(self):
		return self._cache

class Earnest(object):
	def __init__(self, levels):
		self._history = History(levels)

	def consume(self, values):
		self._history.consume(values)

	@staticmethod
	def _find_longest_segment(values):
		""" Finds the longest section of consecutive True entries in values."""
		q = np.array([0,] + list(1*values) + [0,])
		diff = q[1:]-q[:-1]
		ups = np.where(diff == 1)[0]
		dns = np.where(diff == -1)[0]
		if len(ups) == 0:
			return slice(0, 0)
		seq_index = np.argmax(dns-ups)

		return slice(ups[seq_index], dns[seq_index])

	@staticmethod
	def _find_optimal(values, variances):
		""" Selection of the stationary values. """

		# Edge case if only two segment sizes are available
		if len(values) == 2 and np.allclose(variances[-1:], 0):
			return 0

		stddevs = np.sqrt(variances)
		upper = np.array([u >= v if not (np.isnan(u) or np.isnan(v)) else False for u, v in zip((values + stddevs)[1:], values[:-1])])
		lower = np.array([l <= v if not (np.isnan(l) or np.isnan(v)) else False for l, v in zip((values - stddevs)[1:], values[:-1])])

		acceptable = Earnest._find_longest_segment(upper & lower)
		if len(variances[acceptable]) == 0:
			return None
		optimal = variances[acceptable].argmin()
		return range(len(values))[acceptable][optimal]

	def _statistical_inefficiency(self):
		total_variance = self._history.cache['total'].variance
		total_m4 = self._history.cache['total']._M4
		total_n = float(len(self._history.cache['total']))

		segment_sizes, inefficiencies, uncertainties = [], [], []

		for level in self._history.active_levels[:]:
			segment_length = 2**level
			averages = [_.average for _ in self._history.cache[level]]
			if len(averages) == 0:
				continue
			average = np.average(np.array(averages))
			if len(averages) == 1: # TODO document case
				sigma_sq = 0.0
			else:
				sigma_sq = np.var(averages, ddof=1)
			mu_4 = np.average((averages - average)**4)
			inefficiency = segment_length * sigma_sq / total_variance

			# Uncertainties of inefficiency
			n = float(len(averages))
			if len(averages) == 1: #TODO: document case
				uncertainty = 0.
			else:
				var_y = mu_4 / n - sigma_sq**2*(n-3)/(n*(n-1))
				var_x = total_m4 / total_n - total_variance**2*(total_n - 3) / (total_n*(total_n - 1))
				C = total_variance / sigma_sq
				uncertainty = var_x / (2*C) - var_y
			uncertainty = segment_length * np.sqrt(uncertainty) / total_variance

			# collect
			segment_sizes.append(segment_length)
			inefficiencies.append(inefficiency)
			uncertainties.append(uncertainty)

		# select best segment length
		segment_sizes, inefficiencies, uncertainties = map(np.array, (segment_sizes, inefficiencies, uncertainties))
		selected = Earnest._find_optimal(inefficiencies, uncertainties**2)

		return segment_sizes, inefficiencies, uncertainties, selected

	def _rca(self, selected):
		""" Walks backwards for the selected block size and applies the RCA method.

		Parameters
		----------
		selected:
			Index of the level selected for analysis from the history and cache."""

		level = self._history.active_levels[selected]
		cache = self._history.cache[level]

		pval = 0.75
		reverse_averages = [_.average for _ in cache[::-1]]

		# Find limit of normal averages
		valid = None
		for segment in range(3, min(20, len(reverse_averages))):
			r = stq.adfuller(reverse_averages[:segment], maxlag=segment - 2)
			if r[1] > pval:
				valid = segment
		for segment in range(20, len(reverse_averages)):
			s, p = sts.normaltest(reverse_averages[:segment])
			if p > pval:
				valid = segment
		if len(reverse_averages) < 3:
			raise ValueError('Too few equilibrated segments: time series too short or too little history levels allowed.')
		if valid is None:
			raise ValueError('Time series not converged.')

		# Collect properties of the valid segments
		aggregate = sum(cache[-valid:-1], cache[-1])
		numpoints = float(len(aggregate))
		varvar = np.sqrt(aggregate._M4 / numpoints - aggregate.variance**2*(numpoints - 3)/(numpoints*(numpoints - 1)))
		return aggregate.average, aggregate.variance, varvar, numpoints

	def _delta_average(self, selected, numpoints):
		estimates = []
		stddevs = []

		for level in self._history.active_levels[selected:]:
			segment_length = 2**level
			averages = [_.average for _ in self._history.cache[level][-int(numpoints/segment_length):]]
			if len(averages) < 2:
				break
			variance = np.var(averages, ddof=1)
			estimates.append(variance/(len(averages)-1))
			stddevs.append(np.sqrt(2./(len(averages)-1)) * estimates[-1])

		estimates, stddevs = np.array(estimates), np.array(stddevs)
		try:
			optimal = Earnest._find_optimal(estimates, stddevs**2)
		except:
			# No estimate available, but TS converged
			return None
		return np.sqrt(estimates[optimal])

	def evaluate(self):
		""" Estimates the results for the data read in so far.

		Returns
		-------
		average : float
			The estimated value of the equilibrated average of the time series.
		delta_average : float
			The estimated uncertainty of the average due to finite sampling.
		variance : float
			The estimated value of the equilibrated variance of the time series (not the error of the average!)
		delta_variance : float
			The estimated uncertainty of the variance due to finite sampling.
		numpoints : integer
			The number of data points that have been found to be equilibrated (as seen from the end).

		Raises
		------
		ValueError
			If the time series is not converged."""
		self._history.build_cache()
		block_sizes, inefficiencies, uncertainties, selected = self._statistical_inefficiency()
		if selected is None:
			self._history.clear_cache()
			raise ValueError('Time series not converged.')

		average, variance, delta_variance, numpoints = self._rca(selected)
		delta_average = self._delta_average(selected, numpoints)
		self._history.clear_cache()
		return average, delta_average, variance, delta_variance, numpoints

def _command_line():
	import fileinput

	e = Earnest(7)
	for line in fileinput.input():
		e.consume(float(line))
	print e.evaluate()


if __name__ == '__main__':
	e = Earnest(7)
	data = np.random.normal(size=8)
	e.consume(data)
	e.evaluate()