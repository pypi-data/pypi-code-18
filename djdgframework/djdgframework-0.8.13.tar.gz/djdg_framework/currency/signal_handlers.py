#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
author lilx
created on 2017/5/15
 """
from __future__ import unicode_literals, absolute_import
from django.db import transaction
from djdg_framework.currency.models import PointAccount
from djdg_framework.currency.models import PointBill
import copy


@transaction.atomic
def point_event_handler(sender, **kwargs):
    """
    积分事件入口
    :param sender:
    :param kwargs: {
        'user_id': '',
        'operate_type': '',
        'change_point': '',
        'increase_type': '',
        'increase_rule_id': '',
        'order_id': '',
        'order_item_id': '',
        'remark': ''
    }
    :return:
    """
    event = kwargs['event']
    user_id = event['user_id']
    account = PointAccount.objects.filter(user_id=user_id).select_for_update().first()
    if not account:
        account = PointAccount.objects.create(user_id=user_id)
    bill = copy.deepcopy(event)
    bill['account'] = account
    change_point = bill['change_point']
    if 1 == bill['operate_type']:
        change_point = -change_point
    account.point += change_point
    account.balance += change_point
    bill['point'] = account.point
    bill['balance'] = account.balance
    PointBill.objects.create(**bill)
    account.save()
    return True
