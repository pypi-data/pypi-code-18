# -*- coding: utf-8 -*-

from collections import Counter, defaultdict

class AppendedStrCounter(Counter):
    def __init__(self, iter, str_to_append):
        self._appended_str = str_to_append
        super(AppendedStrCounter, self).__init__(iter)
    def __setitem__(self, key, value):
        if len(key) > 1 and not key.endswith(self._appended_str):
            key += self._appended_str
        super(AppendedStrCounter, self).__setitem__(tuple(key), value)
