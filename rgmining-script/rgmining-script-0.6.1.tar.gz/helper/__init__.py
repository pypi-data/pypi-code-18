#
# helper/__init__.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-script.
#
# rgmining-script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-script. If not, see <http://www.gnu.org/licenses/>.
#
"""Helper modules.

This module exports two variables, :data:`ALGORITHMS <algorithms.ALGORITHMS>`
and :data:`DATASETS <datasets.DATASETS>`, and two functions
:meth:`graph() <algorithms.graph>` and :meth:`load() <datasets.load>`.
See each document for more information.
"""
from __future__ import absolute_import
from helper.algorithms import ALGORITHMS
from helper.datasets import DATASETS
from helper.algorithms import graph
from helper.datasets import load
