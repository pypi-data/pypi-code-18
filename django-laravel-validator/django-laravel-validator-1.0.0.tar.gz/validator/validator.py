# -*- coding: utf-8 -*-
# PROJECT : picopico
# TIME    : 17-1-5 下午12:06
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from importlib import import_module
from django.core.exceptions import ImproperlyConfigured
try:
    from django.utils.translation import ugettext as _
    _('are you sure?')
except ImproperlyConfigured:
    def _(s): return s

import re
from validator.exceptions import NeedParamsException


def filte_rules(rules):
    ret = {}
    for name, value in rules.items():
        if not name.startswith('__') and isinstance(value, str):
            ret.update({name: value})

    return ret


class BaseValidator(type):

    def __new__(mcs, name, base, dicts):
        clazz = type.__new__(mcs, name, base, dicts)
        clazz.rules = filte_rules(dicts)
        clazz.messages = dicts.get('messages', None)
        return clazz


class Validator(object, metaclass=BaseValidator):

    def __init__(self, data, request=None):
        self.__messages = {}
        self.status = True
        self.data = data
        self.request = request

    def validate(self):
        for k, v in self.data.items():
            self.__check_data__(k, v)

        if self.status:
            if getattr(self, 'check', None) and callable(getattr(self, 'check')):
                self.check()

    def get_messages(self):
        return {'status': self.status, 'messages': self.__messages}

    def set_messages(self, message):
        self.__messages.update(message)

    def __parse_rules__(self, name):
        rule_str = self.rules.get(name, None)
        if rule_str:
            rules = rule_str.split('|')
            rule_with_params = map(self.__parse_rule_parameters__, rules)
            return rule_with_params
        else:
            return []

    @staticmethod
    def __parse_rule_parameters__(rule):
        rule_name = rule.split(':')[0]
        ret = {'name': rule_name.strip()}

        if len(rule.split(':')) > 1:
            parameters = map(lambda s: s.strip(), filter(lambda s: s, rule.split(':')[1].split(',')))
            ret['parameters'] = parameters

        return ret

    def __check_data__(self, name, value):
        rules = self.__parse_rules__(name)
        for rule in rules:
            rule_name = rule.get('name', None)
            rule_class = VALIDATOR_RULES.get(rule_name, None)
            if rule_class:
                if self.messages:
                    message = self.messages[name][rule_name]
                else:
                    message = None

                if rule.get('parameters', None):
                    ruler = rule_class(value, *rule.get('parameters'), message=message)
                else:
                    ruler = rule_class(value, message=message)
                if not ruler.status:
                    self.status = False
                    if not self.__messages.get(name, None):
                        self.__messages[name] = {}
                    self.__messages[name][ruler.name] = ruler.get_message()
            else:
                raise Exception(_('{VALUE} rule not found').format(VALUE=rule))

    def get(self, item):
        return self.data.get(item)


class BaseRule:
    value = None
    message = None
    name = None
    params = None
    status = False

    def check(self):
        raise NotImplementedError

    def __init__(self, value, *params, message=None):
        if message:
            self.message = message

        self.value = value
        self.params = params
        self.check()

    def get_message(self, message=None):
        if message:
            self.message = message

        return self.message.format(VALUE=self.value)


class BaseRegexRule(BaseRule):
    def regex_check(self):
        r = re.compile(self.regex)
        return True if r.match(self.value) else False

    def check(self):
        pass


class RegexRule(BaseRegexRule):
    name = 'regex'
    message = _('{VALUE} is not suite the given regex')
    regex = r''

    def check(self):
        if self.params and self.params[0]:
            self.regex = self.params[0]
        else:
            raise NeedParamsException('missing regex parameter')

        if self.value and self.regex_check():
            self.status = True
        else:
            self.status = False

    def get_message(self, message=None):
        if message:
            self.message = message
        return self.message.format(VALUE=self.value, REGEX=self.regex)


class AlphabetRule(BaseRegexRule):
    name = 'alphabet'
    message = _('{VALUE} is not alphabet')
    regex = r'[a-zA-Z]+'

    def check(self):
        self.build_regex()
        if self.value and self.regex_check():
            self.status = True
        else:
            self.status = False

    def regex_check(self):
        return True if re.fullmatch(self.regex, self.value) else False

    def build_regex(self):
        if not self.params:
            return
        if 1 == len(self.params):
            self.regex = r'[a-zA-Z]{' + self.params[0] + r'}'
        if 2 == len(self.params):
            self.regex = r'[a-zA-Z]{' + self.params[0] + r',' + self.params[1] + r'}'


class EmailRule(BaseRegexRule):
    name = 'email'
    message = _('{VALUE} is not an email address')
    regex = r'[^@]+@[^@]+\.[^@]+'

    def check(self):
        if self.value and self.regex_check():
            self.status = True
        else:
            self.status = False


class NumbericRule(BaseRegexRule):
    name = 'numberic'
    message = _('{VALUE} is not numberic')
    regex = r'[0-9]+'

    def check(self):
        self.build_regex()
        if self.value and self.regex_check():
            self.status = True
        else:
            self.status = False

    def build_regex(self):
        if not self.params:
            return
        if 1 == len(self.params):
            self.regex = r'[0-9]{' + self.params[0] + r'}'
        if 2 == len(self.params):
            self.regex = r'[0-9]{' + self.params[0] + r',' + self.params[1] + r'}'

    def regex_check(self):
        return True if re.fullmatch(self.regex, self.value) else False


class RequiredRule(BaseRule):
    name = 'required'
    message = _('value is required')

    def check(self):
        self.status = True if self.value else False


class MinRule(BaseRule):
    name = 'min'
    message = _('[{VALUE}] is must longer than {PARAM}')

    def check(self):
        if self.params:
            if len(self.value) < int(self.params[0]):
                self.status = False
            else:
                self.status = True
        else:
            raise NeedParamsException('min value')

    def get_message(self, message=None):
        if message:
            self.message = message
        return self.message.format(VALUE=self.value, PARAM=self.params[0])


class MaxRule(BaseRule):
    name = 'max'
    message = _('[{VALUE}] is shorter than {PARAM}')

    def check(self):
        if self.params:
            if len(self.value) > int(self.params[0]):
                self.status = False
            else:
                self.status = True
        else:
            raise NeedParamsException('max value')

    def get_message(self, message=None):
        if message:
            self.message = message
        return self.message.format(VALUE=self.value, PARAM=self.params[0])


class UniqueRule(BaseRule):
    name = 'unique'
    message = _('[{VALUE}] in model {MODEL} field {FIELD} is not unique')

    def check(self):
        if self.params and len(self.params) > 1:
            model_name = self.params[0]
            obj_name = self.params[1]
            field = self.params[2]
            try:
                model = import_module(model_name)
                obj = getattr(model, obj_name, None)
                ret = obj.objects.filter(**{field: self.value})
                if ret:
                    self.status = False
                else:
                    self.status = True
            except ImportError:
                raise ImportError(model_name + ' object not found ')

        else:
            raise NeedParamsException('table name and column name')

    def get_message(self, message=None):
        if message:
            self.message = message
        return self.message.format(VALUE=self.value,
                                   MODEL=self.params[0] + '.' + self.params[1],
                                   FIELD=self.params[2])


class ExistRule(BaseRule):
    name = 'exist'
    message = _('[{VALUE}] in model {MODEL} field {FIELD} is not exist')

    def check(self):
        if self.params and len(self.params) > 1:
            model_name = self.params[0]
            obj_name = self.params[1]
            field = self.params[2]
            try:
                model = import_module(model_name)
                obj = getattr(model, obj_name, None)
                ret = obj.objects.filter(**{field: self.value})
                if ret:
                    self.status = True
                else:
                    self.status = False
            except ImportError:
                raise ImportError(model_name + ' object not found ')

        else:
            raise NeedParamsException('table name and column name')

    def get_message(self, message=None):
        if message:
            self.message = message

        return self.message.format(VALUE=self.value,
                                   MODEL=self.params[0] + '.' + self.params[1],
                                   FIELD=self.params[2])


VALIDATOR_RULES = {'alphabet': AlphabetRule,
                   'numberic': NumbericRule,
                   'required': RequiredRule,
                   'min': MinRule,
                   'max': MaxRule,
                   'unique': UniqueRule,
                   'exist': ExistRule,
                   'regex': RegexRule,
                   'email': EmailRule}
