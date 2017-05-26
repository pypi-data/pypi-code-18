#!/usr/bin/env python
# vi: et sw=2 fileencoding=utf-8
#============================================================================
# pitargparse
# Copyright (c) 2017 Pispalan Insinööritoimisto Oy (http://www.pispalanit.fi)
#
# Redistributions of files shall retain the above copyright notice.
#
# @created     26.05.2017
# @author      Harry Karvonen <harry.karvonen@pispalanit.fi>
# @copyright   Copyright (c) Pispalan Insinööritoimisto Oy
# @license     MIT Licence
#============================================================================

from __future__ import unicode_literals

import argparse
import os


class NoOverWriteFileType(argparse.FileType):
  # XXX documentation


  def __call__(self, string):
    if os.path.exists(string):
      raise argparse.ArgumentTypeError("File '%s' exists" % string)

    return super(NoOverWriteFileType,self).__call__(string)
    # def __call__


  # class NoOverWriteFileType


class PITArgumentParser(argparse.ArgumentParser):
  # XXX documentation
  """

Source: http://stackoverflow.com/questions/15782948/how-to-have-sub-parser-arguments-in-separate-namespace-with-argparse
"""


  def parse_args(self, *args, **kw):
    res = argparse.ArgumentParser.parse_args(self, *args, **kw)
    from argparse import _HelpAction, _SubParsersAction
    for x in self._subparsers._actions:
      if not isinstance(x, _SubParsersAction):
        continue
      if x.dest == "==SUPPRESS==":
        raise RuntimeError("use dest in add_subparsers")
      v = x.choices[getattr(res, x.dest)] # select the subparser name
      subparseargs = {}
      for x1 in v._optionals._actions: # loop over the actions
        if isinstance(x1, _HelpAction): # skip help
          continue
        n = x1.dest
        if hasattr(res, n): # pop the argument
          subparseargs[n] = getattr(res, n)
          delattr(res, n)
      res.subparseargs = subparseargs
    return res
    # def parse_args


  # class PITArgumentParser


