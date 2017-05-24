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
from ..utils import *
from ..exceptions import BoardFormatException

class BoardFormat(object):
    def to_string(self, board, **kwargs):
        out = StringIO()
        self.dump(board, out, **kwargs)
        res = out.getvalue()
        out.close()
        return res
    def from_string(self, s, board=None):
        from . import Board
        if board is None:
            board = Board()
        f = StringIO(s)
        self.load(board, f)
        f.close()
        return board
