#! /usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (C) 2017 贵阳货车帮科技有限公司
#

import unittest
from hbt import get_level_count, get_commit_file_list, get_problem_count, get_commit_summary
from hbt import LEVEL_ERROR, LEVEL_WARN

class HbtTestCase(unittest.TestCase):
  def test_get_level(self):
    problems = """
      Starting audit...
      [WARN] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:205: 本行字符数 105个，最多：100个。 [LineLength]
      [WARN] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:208: 本行字符数 110个，最多：100个。 [LineLength]
      [WARN] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:268: 本行字符数 132个，最多：100个。 [LineLength]
      [WARN] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:281:34: 避免空行。 [EmptyStatement]
      [ERROR] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:292: 本行字符数 138个，最多：100个。 [LineLength]
      Audit done.
    """

    self.assertEquals(4, get_level_count(problems, LEVEL_WARN))
    self.assertEquals(1, get_level_count(problems, LEVEL_ERROR))

    no_problems = """
      Starting audit...
      Audit done.
    """
    self.assertEquals(0, get_level_count(no_problems, LEVEL_WARN))
    self.assertEquals(0, get_level_count(no_problems, LEVEL_ERROR))

    self.assertEquals(0, get_level_count('', LEVEL_WARN))
    self.assertEquals(0, get_level_count('', LEVEL_ERROR))


  def test_get_commit_file_list(self):
    commit_javas = """
    commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
    Author: ZhouXu <xu.zhou1@56qq.com>
    Date:   Thu May 25 14:59:19 2017 +0800

    fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数。所以目前只支持两位小数转化

M   src/main/java/com/wlqq/checkout/CheckOutActivity.java
D   src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java
A   src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java
M   src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java
R100    debug.java  test.java
    """

    list = get_commit_file_list(commit_javas.split('\n'))
    self.assertEquals(4, len(list))
    self.assertEquals('src/main/java/com/wlqq/checkout/CheckOutActivity.java', list[0])
    self.assertEquals('src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java', list[1])
    self.assertEquals('src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java', list[2])
    self.assertEquals('test.java', list[3])

    without_javas = """
    commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
    Author: ZhouXu <xu.zhou1@56qq.com>
    Date:   Thu May 25 14:59:19 2017 +0800

    fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数。所以目前只支持两位小数转化

    build.gradle
    src/main/res/layout/item_list_shift_order_detail.xml
    src/main/res/values/dimens.xml
    src/main/res/values/strings.xml
    src/main/res/values/styles.xml
    """
    list = get_commit_file_list(without_javas.split('\n'))
    self.assertEquals(0, len(list))

    list = get_commit_file_list([])
    self.assertEquals(0, len(list))


  def test_get_commit_summary(self):
    commit_msgs = """
    commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
    Author: ZhouXu <xu.zhou1@56qq.com>
    Date:   Thu May 25 14:59:19 2017 +0800

    fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数

M   src/main/java/com/wlqq/checkout/CheckOutActivity.java
D   src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java
A   src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java
M   src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java
    """

    summary = get_commit_summary(commit_msgs.split('\n'))
    self.assertEquals('fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数', summary)


    missed_summary = """
    commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
    Author: ZhouXu <xu.zhou1@56qq.com>
    Date:   Thu May 25 14:59:19 2017 +0800

    """
    summary = get_commit_summary(missed_summary.split('\n'))
    self.assertIsNone(summary)

    summary = get_commit_summary([])
    self.assertIsNone(summary)


  def test_get_problem_count(self):
    self.assertEquals(2, get_problem_count(['TestHasWarns.java']))
    self.assertEquals(0, get_problem_count(['TestNoWarn.java']))


if __name__ == '__main__':
  unittest.main()
