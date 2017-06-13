# -*- coding: utf-8 -*-

"""
This file is part of eyelinkparser.

eyelinkparser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

eyelinkparser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with datamatrix.  If not, see <http://www.gnu.org/licenses/>.
"""

from eyelinkparser import EyeLinkParser


class EyeTribeParser(EyeLinkParser):
	
	def __init__(self, **kwargs):
		
		if u'ext' not in kwargs:
			kwargs[u'ext'] = u'.tsv'
		EyeLinkParser.__init__(self, **kwargs)
		
	def split(self, line):
	
		l = EyeLinkParser.split(self, line)
		if not l:
			return l
		# Convert messages to EyeLink format
		if l[0] == u'MSG':
			l = l[3:]
			l.insert(0, u'MSG')
			return l
		# Convert samples to EyeLink format:		
		if len(l) == 24:
			l = [l[2], l[7], l[8], l[9], u'...']
			return l
		return l
