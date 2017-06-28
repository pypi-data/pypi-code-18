#!/usr/bin/env python
# -*- coding: utf-8 -*-
import enum


class TaskType(enum.IntEnum):
    unknown = 0
    macaca_test = 1
    ui_recorder = 2
    macaca_server = 3
