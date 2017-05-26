# -*- coding: utf-8 -*-
# PROJECT : picopico
# TIME    : 17-1-14 下午1:42
# AUTHOR  : shenyangang <email:shenyangang@163.com>


class RuleExcception(Exception):
    message = None

    def __init__(self, message):
        if message:
            self.message = message

    def __str__(self):
        return self.message


class NeedParamsException(RuleExcception):
    message = 'this rule need params : {PARAMS}'
    params = ''

    def __init__(self, params):
        if params:
            self.params = params

    def __str__(self):
        return self.message.format(PARAMS=self.params)
