#  -*- coding: utf-8 -*-
# *****************************************************************************
# Prism CLI
# Copyright (c) 2017 by the Prism CLI authors (see AUTHORS)

# Module authors:
#   Trevin Miller <stumblinbear@gmail.com>
#
# *****************************************************************************

import os


def get(name, formatting={}):
    with open(os.path.join(os.path.dirname(__file__), 'templates', name + '.pl8')) as file:
        return ''.join(file.readlines()).format(**formatting)
