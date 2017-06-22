#! /usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (C) 2017 贵阳货车帮科技有限公司
#

import re
import os
import sys
import subprocess
import platform

# checkstyle problem level
LEVEL_ERROR = 'ERROR'
LEVEL_WARN = 'WARN'

CHECKSTYLE_JAR_FILE_NAME = 'checkstyle-all.jar'
CHECKSTYLE_CONFIG_FILE_NAME = 'checkstyle-config.xml'

JAVA_FILE_POSTFIX = '.java'
DELETE_FILE_PREFIX = 'D'
MOVE_FILE_PREFIX = 'R'
DATE_PREFIX = 'Date:'
CHECKSTYLE_TAG = '[checked_style] '

CYGWIN_SYSTEM_PREFIX = 'CYGWIN'


# the count of level, like ERROR, WARN
# such as '[WARN] D:\git_workspace\GasStationMerchant\GasStationMerchantApp\src\main\java\com\wlqq\checkout\CheckOutActivity.java:205'
def get_level_count(lines, level):
  return len(re.compile(r"\[%s\]" % level).findall(lines))


# output example:
#   commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
#   Author: ZhouXu <xu.zhou1@56qq.com>
#   Date:   Thu May 25 14:59:19 2017 +0800
#
#   fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数。所以目前只支持两位小数转化
#
#   M  src/main/java/com/wlqq/checkout/CheckOutActivity.java
#   D  src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java
#   A  src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java
#   M  src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java
#   R100    debug.java  test.java
#
# 获取java文件名列表
def get_commit_file_list(lines):

  list = []
  for line in lines:
    line = line.strip()

    if line.find(JAVA_FILE_POSTFIX) != -1:
      strs = re.split('\s+', line)

      if strs[0] == DELETE_FILE_PREFIX:
        # 'D  src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java'
        continue

      if strs[0].startswith(MOVE_FILE_PREFIX):
        # 'R100    debug.java  test.java'
        list.append(strs[2])
      else:
        # 'M  src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java' 或者
        # 'A  src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java'
        list.append(strs[1])

  return list


# output example:
#   commit 0bf74b02b7f9be98ebc5bddd59e71f95f2585633
#   Author: ZhouXu <xu.zhou1@56qq.com>
#   Date:   Thu May 25 14:59:19 2017 +0800
#
#   fix: 浮点数转化为长整型导致误差。目前前端已经限制只支持两位小数。所以目前只支持两位小数转化
#
#   M  src/main/java/com/wlqq/checkout/CheckOutActivity.java
#   D  src/main/java/com/wlqq/shift/activity/FixShiftSuccessActivity.java
#   A  src/main/java/com/wlqq/shift/activity/UnConfirmedShiftActivity.java
#   M  src/main/java/com/wlqq/shift/adapter/ConfirmOilPriceAdapter.java
#
# 获取Date后面的第一个非空行
def get_commit_summary(lines):

  has_found_date = False

  for line in lines:
    line = line.strip()

    if has_found_date and len(line) > 0:
      return line

    if line.find(DATE_PREFIX) != -1:
      has_found_date = True

  else:
    return None


def get_problem_count(javas):
  hbt_dir = subprocess.check_output('git config hbt.dir', shell=True).strip()

  if platform.system().startswith(CYGWIN_SYSTEM_PREFIX):
    # change to cygwin path
    hbt_dir = subprocess.check_output('cygpath -m "' + hbt_dir + '"', shell=True).strip()

  jar_file = os.path.join(hbt_dir, CHECKSTYLE_JAR_FILE_NAME)
  config_file = os.path.join(hbt_dir, CHECKSTYLE_CONFIG_FILE_NAME)

  # check code command
  command = 'java -jar ' + jar_file + ' -c ' + config_file

  sum = 0
  for java in javas:
    result = subprocess.check_output(command + ' ' + java, shell=True)

    count = get_level_count(result, LEVEL_ERROR)
    count += get_level_count(result, LEVEL_WARN)
    if count > 0:
      print "\n checkstyle failed: " + java

    sum += count

  return sum


def main():
  print '\n....Code Style Checking....\n'

  commit_log = subprocess.check_output('git log --name-status -n 1', shell=True)

  lines = commit_log.split('\n')
  commit_javas = get_commit_file_list(lines)
  summary = get_commit_summary(lines)

  count = get_problem_count(commit_javas)

  if count > 0:
    print '\n....You must fix the errors and warnings first, then post review again....\n'
    sys.exit(-1)

  # ignore the first argv
  rbt_command = 'rbt ' + ' '.join(sys.argv[1:])
  if summary:
    rbt_command += ' --summary "' + CHECKSTYLE_TAG + summary + '"'

  print 'running command: ' + rbt_command
  subprocess.call(rbt_command, shell=True)


if __name__ == '__main__':
  main()

