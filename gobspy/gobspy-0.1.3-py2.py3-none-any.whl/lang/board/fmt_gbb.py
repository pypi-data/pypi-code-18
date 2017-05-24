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

import re

from ..utils import *
from ..i18n import translate as t
from ..builtins.types.color import NUM_COLORS, I18N_COLORS_BY_NAME, Color
from .basic import BoardFormatException, BoardFormat

def is_numeric(x):
  return re.match('^[0-9]+$', x)

class GbbBoardFormat(BoardFormat):
  "Simple human-friendly board format."

  def dump(self, board, f, style='verbose', **kwargs):
    if style == 'verbose':
      self.dump_with_translator(board, f, self.verbose_translator)
    elif style == 'compact':
      self.dump_with_translator(board, f, self.compact_translator)
    else:
      assert False

  def verbose_translator(self, s):
    return s

  def compact_translator(self, s):
    _dict = {
      'cell': 'o',
      'size': 's',
      'head': 'x',
    }
    if s in _dict:
      return _dict[s]
    else:
      return s[0]

  def dump_with_translator(self, board, f, translate):
    w, h = board.size
    f.write('GBB/1.0\r\n')
    f.write('%s %i %i\r\n' % (translate('size'), w, h))
    for x in range(w):
      for y in range(h):
        cell = []
        for coli in range(4):
          cant = board.cells[y][x].num_stones(coli)
          if cant == 0: continue
          col = Color(coli).i18n_name()
          cell.append('%s %i' % (translate(col), cant))
        if cell == []: continue
        f.write('%s %i %i %s\r\n' % (translate('cell'), x, y, ' '.join(cell)))
    y, x = board.head
    f.write('%s %i %i\r\n' % (translate('head'), x, y))
    f.write('%%\r\n')

  def load(self, board, f):

    orig = ['']

    f_lines = read_stripped_lines(f)

    def next_line():
      if f_lines == []:
        return False
      else:
        orig[0] = f_lines.pop(0)
        return orig[0].split(' ')

    def fail(msg):
      raise BoardFormatException(t('Malformed gbb board') + '\n' +
                                 '  ' + t('Near line:') + ' "' + orig[0].strip('\r\n') + '"\n' +
                                 '  ' + msg)

    # GBB header
    l = next_line()
    if l != ['GBB/1.0']:
      fail(t('Expected header line "GBB/1.0"'))

    l = next_line()
    if len(l) == 3 and l[0] in ['size', 's'] and is_numeric(l[1]) and is_numeric(l[2]):
      width, height = board.size = int(l[1]), int(l[2])
    else:
      fail(t('Expected board size line "size <width> <height>"'))

    board.randomize_header()
    board._clear_board()

    color_to_index = I18N_COLORS_BY_NAME

    visited_cells = {}

    while True:
      l = next_line()
      if not l: break
      if l[0] in ['head', 'x']:
        if len(l) == 3 and is_numeric(l[1]) and is_numeric(l[2]):
          x, y = int(l[1]), int(l[2])
          if x >= width or y >= height:
            fail(t('"head %u %u" out of bounds') % (x, y))
          board.head = y, x
        else:
          fail(t('Expected head line "head <x> <y>"'))
      elif l[0] in ['cell', 'o']:
        if len(l) >= 3 and is_numeric(l[1]) and is_numeric(l[2]):
          x, y = int(l[1]), int(l[2])
          if (x, y) in visited_cells:
            fail(t('Cell (%u,%u) is repeated.') % (x, y))
          visited_cells[(x, y)] = True
          count_col = {}
          rest = l[3:]
          while rest != []:
            color_name = rest[0].capitalize()
            coli = None
            for k in color_to_index.keys():
                if color_name == k or k[0] == color_name[0]:
                    coli = color_to_index[k]

            if len(rest) >= 2 and not coli is None and is_numeric(rest[1]):
              rest.pop(0)
              count_col[coli] = count_col.get(coli, 0) + int(rest.pop(0))
            else:
              fail(t('Expected cell line "cell <x> <y> [<color> <num>]*"'))
          for k, v in count_col.items():
            board.set_num_stones(y, x, k, v)
        else:
          fail(t('Expected cell line "cell <x> <y> [<color> <num>]*"'))
      else:
        fail(t('Expected head line "head <x> <y>" or cell line "cell <x> <y> [<color> <num>]*"'))
