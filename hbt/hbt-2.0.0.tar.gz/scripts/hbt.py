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
import time

# checkstyle problem level
LEVEL_ERROR = 'ERROR'
LEVEL_WARN = 'WARN'

CHECKSTYLE_JAR_FILE_NAME = 'checkstyle-all.jar'
CHECKSTYLE_CONFIG_FILE_NAME = 'checkstyle-config.xml'

JAVA_FILE_SUFFIX = '.java'
XML_FILE_SUFFIX = '.xml'

# example: "M  src/main/java/com/wlqq/checkout/CheckOutActivity.java"
# example: "A  src/main/res/values/strings.xml"
ADD_OR_MODIFY_PATTERN = re.compile(r'^\s*[M|A]\s+(.+[\.java|\.xml])\s*$')
# example: "R100    debug.java  test.java"
# example: "R109    src.xml  dest.xml"
RENAME_PATTERN = re.compile(r'^\s*R\d+\s+.+[\.java|\.xml]\s+(.+[\.java|\.xml])\s*$')

GROUP_INDEX_FILE_NAME = 1

DATE_PREFIX = 'Date:'
CHECKSTYLE_TAG = '[checked_style_2] '

CYGWIN_SYSTEM_PREFIX = 'CYGWIN'

# the first line of java body MUST be package declaration.
# for example: package com.wlqq.app;
JAVA_BODY_PATTERN = re.compile(r'^package.+$')
# the first line of java body MUST be body tag.
# for example:
#    <resources>
#    <selector xmlns:android="http://schemas.android.com/apk/res/android">
#    <LinearLayout
XML_BODY_PATTERN = re.compile(r'^<[a-zA-Z].+$')

XML_COPYRIGHT_TEMPLATE ="""\
<?xml version="1.0" encoding="utf-8"?>
<!-- Copyright (C) {} 贵阳货车帮科技有限公司 -->\n
"""

JAVA_COPYRIGHT_TEMPLATE ="""\
/*
 * Copyright (C) {} 贵阳货车帮科技有限公司
 */\n
"""


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
#   A  src/main/res/values/strings.xml
#   R100    debug.java  test.java
#
# 获取java文件名列表
def get_commit_file_list(lines):

  list = []
  for line in lines:
    result = RENAME_PATTERN.match(line)
    if result:
      list.append(result.group(GROUP_INDEX_FILE_NAME))
      continue

    result = ADD_OR_MODIFY_PATTERN.match(line)
    if result:
      list.append(result.group(GROUP_INDEX_FILE_NAME))

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


def get_problem_count(files):
  hbt_dir = subprocess.check_output('git config hbt.dir', shell=True).strip()

  if platform.system().startswith(CYGWIN_SYSTEM_PREFIX):
    # change to cygwin path
    hbt_dir = subprocess.check_output('cygpath -m "' + hbt_dir + '"', shell=True).strip()

  jar_file = os.path.join(hbt_dir, CHECKSTYLE_JAR_FILE_NAME)
  config_file = os.path.join(hbt_dir, CHECKSTYLE_CONFIG_FILE_NAME)

  # check code command
  command = 'java -jar ' + jar_file + ' -c ' + config_file

  sum = 0
  for file in files:
    if is_java_file(file):
      print 'checking file: ' + file
      result = subprocess.check_output(command + ' ' + file, shell=True)

      count = get_level_count(result, LEVEL_ERROR)
      count += get_level_count(result, LEVEL_WARN)
      if count > 0:
        print "\n checkstyle failed: " + file

      sum += count

  return sum


def get_create_year(file):
  command = 'git log --follow --format=%ai --reverse -- {} | head -1'.format(file)

  # output example: 2015-11-10 15:44:29 +0800
  date_format = subprocess.check_output(command, shell=True)

  if len(date_format) == 0:
    return get_current_year()

  return date_format.split('-')[0]


def get_current_year():
  return time.strftime('%Y', time.localtime(time.time()))


def get_copyright(is_java, start, end):
  template = XML_COPYRIGHT_TEMPLATE

  if is_java:
    template = JAVA_COPYRIGHT_TEMPLATE

  if start == end:
    return template.format(start)

  return template.format(start + ' - ' + end)


def is_java_file(file):
  return file.find(JAVA_FILE_SUFFIX) != -1


def is_xml_file(file):
  return file.find(XML_FILE_SUFFIX) != -1


def is_body_start(is_java, line):
  if is_java:
    return JAVA_BODY_PATTERN.match(line)

  return XML_BODY_PATTERN.match(line)


def update_copyright(file):
  fileRead = open(file, 'r')
  lines = fileRead.readlines()
  fileRead.close()

  fileWrite = open(file, 'w')

  is_java = is_java_file(file)
  copyright = get_copyright(is_java, get_create_year(file), get_current_year())
  fileWrite.write(copyright)

  # skip until file body line
  need_skip = True
  for line in lines:
    if need_skip and is_body_start(is_java, line):
      need_skip = False

    if need_skip:
      continue;

    fileWrite.write(line)

  fileWrite.close()


def update_copyright_for_all(files):
  for file in files:
    print 'updating file: ' + file
    update_copyright(file)


def has_pending_changes():
  return '' != subprocess.check_output('git status --porcelain --untracked-files=no', shell=True)


def is_update_copyright_only(command):
  return 'copyright' == command


def get_files(dir):
  list = []
  for root, dirs, files in os.walk(dir):
    for file in files:
      if is_java_file(file) or is_xml_file(file):
        list.append(os.path.join(root, file))

  return list


def check_argv(args):
  if len(args) != 3 or not os.path.isdir(args[2]):
    print 'Usage: hbt copyright <source_dir>'
    sys.exit(-1)


def main():
  update_only = is_update_copyright_only(sys.argv[1])

  if update_only:
    # format: hbt copyright <source_dir>
    check_argv(sys.argv)

    files = get_files(sys.argv[2])
    update_copyright_for_all(files)
    return

  commit_log = subprocess.check_output('git log --name-status -n 1', shell=True)

  lines = commit_log.split('\n')
  summary = get_commit_summary(lines)

  commit_files = get_commit_file_list(lines)
  update_copyright_for_all(commit_files)

  if has_pending_changes():
    print '\nWARNING: 有未commit的文件。可能是被自动更新了copyright。请commit后再次发送review request'
    sys.exit(-1)

  count = get_problem_count(commit_files)
  if count > 0:
    print '\nWARNING: You must fix the errors and warnings first, then post review again'
    sys.exit(-1)

  # ignore the first argv
  rbt_command = 'rbt ' + ' '.join(sys.argv[1:])
  if summary:
    rbt_command += ' --summary "' + CHECKSTYLE_TAG + summary + '"'

  print 'running command: ' + rbt_command
  subprocess.call(rbt_command, shell=True)


if __name__ == '__main__':
  main()

