#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2017/5/15
 """
from __future__ import unicode_literals, absolute_import
from django.dispatch.dispatcher import Signal
from djdg_framework.currency.signal_handlers import point_event_handler


point_event_signal = Signal(providing_args=['event'])

point_event_signal.connect(point_event_handler)
