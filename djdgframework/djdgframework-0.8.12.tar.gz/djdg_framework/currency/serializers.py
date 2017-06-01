#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2017/5/16
 """
from __future__ import unicode_literals, absolute_import
from rest_framework import serializers
from djdg_framework.currency.models import PointAccount


class PointAccountSerializer(serializers.ModelSerializer):
    """
    积分账户序列化对象
    """
    class Meta:
        model = PointAccount
