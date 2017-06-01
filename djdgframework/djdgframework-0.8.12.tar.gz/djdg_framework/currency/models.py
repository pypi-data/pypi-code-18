#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from djdg_core.models import DateTimeModel


class PointAccount(DateTimeModel):
    """
    积分账户
    """
    user_id = models.IntegerField('用户id，唯一', unique=True)
    point = models.IntegerField('总积分', default=0)
    balance = models.IntegerField('积分余额', default=0)
    consume = models.IntegerField('已消费积分', default=0)


class PointBill(models.Model):
    """
    积分账单
    """
    OPERATE_TYPES = (
        (0, '获得'),
        (1, '消费')
    )

    account = models.ForeignKey(PointAccount, related_name='bills')
    user_id = models.IntegerField('用户id')
    operator_id = models.IntegerField('明细操作者id', null=True, blank=True, default=None)
    operate_type = models.SmallIntegerField('操作类型', choices=OPERATE_TYPES)
    change_point = models.IntegerField('变动积分')
    point = models.IntegerField('总积分')
    balance = models.IntegerField('积分余额', default=0)
    increase_type = models.SmallIntegerField('获取积分条件类型', null=True, blank=True, default=None)
    increase_rule_id = models.IntegerField('获取积分规则id', null=True, blank=True, default=None)
    order_id = models.IntegerField('订单id', null=True, blank=True, default=None)
    order_item_id = models.IntegerField('订单项id', null=True, blank=True, default=None)
    remark = models.CharField(max_length=256, verbose_name='备注', null=True, blank=True, default=None)
    ctime = models.DateTimeField('创建时间', auto_now_add=True)