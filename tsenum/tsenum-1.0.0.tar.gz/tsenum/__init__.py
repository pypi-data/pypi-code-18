# -*- coding: UTF-8 -*-
# vim: noet tabstop=4 shiftwidth=4
#
# Timestamp enumerator 
# Copyright (C) 2016 Alexander Böhm <alxndr.boehm@gmail.com>
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

__version__     = '1.0.0'
__title__		= 'tsenum'
__author__      = 'Alexander Böhm'
__email__		= 'alxndr.boehm@gmail.com'
__license__		= 'GPLv2+'
__description__ = 'Enumerate timestamps from now with offset in different units.'
__epilog__		= 'tsenum v%s, Copyright (C) 2016 %s <%s> Licensed under %s. See source distribution for detailed copyright notices.' % (__version__, __author__, __email__, __license__)

from datetime import datetime, timedelta

def enumerate_times(cur_time, offset, count, step, pattern):
	"""
	>>> from datetime import datetime
	>>> testdate = datetime(year=1970, month=1, day=10)
	>>> enumerate_times(testdate, 0, 3, "day", "%Y-%m-%d")
	['1970-01-10', '1970-01-11', '1970-01-12']
	>>> enumerate_times(testdate, 1, 1, "week", "%Y-%m-%d")
	['1970-01-17']
	>>> enumerate_times(testdate, 3, -1, "day", "%Y-%m-%d")
	['1970-01-12']
	>>> enumerate_times(testdate, 1, 3, "minute", "%Y")
	['1970', '1970', '1970']
	"""

	cur = cur_time
	r = []

	l_count = (count < 0)*count
	h_count = (count >= 0)*count

	if step == None or type(step) != str:
		return []

	elif step.lower() == "week":
		for i in range(l_count, h_count):
			t = cur+timedelta(weeks=(i+offset))
			r += [t.strftime(pattern)]

	elif step.lower() == "day":
		for i in range(l_count, h_count):
			t = cur+timedelta(days=(i+offset))
			r += [t.strftime(pattern)]

	elif step.lower() == "hour":
		for i in range(l_count, h_count):
			t = cur+timedelta(hours=(i+offset))
			r += [t.strftime(pattern)]

	elif step.lower() == "minute":
		for i in range(l_count, h_count):
			t = cur+timedelta(minutes=(i+offset))
			r += [t.strftime(pattern)]

	elif step.lower() == "second":
		for i in range(l_count, h_count):
			t = cur+timedelta(minutes=(i+offset))
			r += [t.strftime(pattern)]

	else:
		return []

	return r

