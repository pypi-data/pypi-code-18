#
# Copyright (C) 2011-2017 Ary Pablo Batista <arypbatista@gmail.com>, Pablo Barenbaum <foones@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#


from .fmt_gbt import GbtBoardFormat
from .fmt_gbb import GbbBoardFormat
from .fmt_html import HtmlBoardFormat
from .fmt_json import JsonBoardFormat

AvailableFormats = {
  'gbt': GbtBoardFormat,
  'gbb': GbbBoardFormat,
  'html': HtmlBoardFormat,
  'json': JsonBoardFormat
}

DefaultFormat = 'gbb'

def is_board_filename(filename):
  return filename.lower().split('.')[-1] in AvailableFormats

def format_for(filename):
  fmt = filename.lower().split('.')[-1]
  if fmt in AvailableFormats:
    return fmt
  else:
    return DefaultFormat
