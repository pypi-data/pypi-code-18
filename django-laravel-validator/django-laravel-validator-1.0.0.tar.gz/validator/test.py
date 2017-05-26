# -*- coding: utf-8 -*-
# PROJECT : picopico
# TIME    : 17-1-5 下午8:59
# AUTHOR  : youngershen <younger.x.shen@gmail.com>
from django.test import TestCase
from validator import Validator


class AlphaTestValidator(Validator):
    text1 = "alphabet"
    text2 = 'alphabet:1'
    text3 = 'alphabet:1,2'

    messages = {
        'text1': {'alphabet': 'is must be alphabet', 'required': 'it is must be required'},
        'text2': {'alphabet': 'is must be alphabet', 'required': 'it is must be required'},
        'text3': {'alphabet': 'is must be alphabet', 'required': 'it is must be required'},
    }

    def check(self):
        self.set_messages({'result': True, 'message': 'ok'})


class RequiredTestValidator(Validator):
    text = 'required'

    messages = {
        'text': {'required': 'it must be required'}
    }

    def check(self):
        self.set_messages({'result': True, 'message': 'ok'})


class MinTestValidator(Validator):
    text = 'min:   5'

    messages = {
        'text': {'min': 'it must longer than {PARAM}'}
    }

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class MaxTestValidator(Validator):
    text = 'max:5'

    messages = {
        'text': {'max': 'it must be shorter than {PARAM}'}
    }

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class UniqueTestValidator(Validator):
    text = 'unique:picopico.apps.account.models,User,cellphone'

    messages = {
        'text': {'unique': 'the {VALUE} is duplicated'}
    }

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class NumbericTestValidator(Validator):
    text1 = 'numberic'
    text2 = 'numberic:1'
    text3 = 'numberic:1,2'

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class RegexTestValidator(Validator):
    text1 = 'regex:[0-9]+'
    text2 = 'regex:[a-z]+'

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class ExistTestValidator(Validator):
    text1 = 'exist:picopico.apps.account.models,User,cellphone'

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


class EmailTestValidator(Validator):
    text1 = 'email'
    text2 = 'email'

    def check(self):
        self.set_messages({'result': True, 'message': 'OK'})


def test_email_validator():
    data1 = {'text1': 'abc@def.com.cn', 'text2': 'abcdef'}
    email_validator_test1 = EmailTestValidator(data1)
    email_validator_test1.validate()
    assert email_validator_test1.status is False
    assert email_validator_test1.get_messages()['messages']['text2']['email'] == 'abcdef is not an email address'

    data2 = {'text1': 'abc@def.com.cn', 'text2': 'a.b.c@def.com.cn'}
    email_validator_test2 = EmailTestValidator(data2)
    email_validator_test2.validate()

    assert email_validator_test2.status is True


def test_alphabet_validator():
    data1 = {'text1': 'abcdef', 'text2': 'a', 'text3': 'ab'}
    alphabet_validator_test1 = AlphaTestValidator(data1)
    alphabet_validator_test1.validate()
    assert alphabet_validator_test1.status, 'status must be True'
    assert alphabet_validator_test1.get_messages()['messages']['result']
    assert alphabet_validator_test1.get_messages()['messages']['message'] == 'ok'

    data2 = {'text1': '123', 'text2': 'ab', 'text3': 'abc'}
    alphabet_validator_test2 = AlphaTestValidator(data2)
    alphabet_validator_test2.validate()
    assert alphabet_validator_test2.status is False, 'status must be False'
    assert len(alphabet_validator_test2.get_messages()['messages']) == 3


def test_required_validator():
    required_validator_test1 = RequiredTestValidator({'text': 'i am here'})
    required_validator_test1.validate()
    assert required_validator_test1.status
    assert required_validator_test1.get_messages()['messages']['result']
    assert required_validator_test1.get_messages()['messages']['message'] == 'ok'

    required_validator_test2 = RequiredTestValidator({'text': ''})
    required_validator_test2.validate()
    assert required_validator_test2.status is False, 'status must be False'
    assert required_validator_test2.get_messages()['messages']['text']['required'] == 'it must be required'


def test_min_validator():
    min_validator_test1 = MinTestValidator({'text': '12345'})
    min_validator_test1.validate()
    assert min_validator_test1.status is True
    assert min_validator_test1.get_messages()['messages']['result'] is True
    assert min_validator_test1.get_messages()['messages']['message'] == 'OK'

    min_validator_test2 = MinTestValidator({'text': '1234'})
    min_validator_test2.validate()
    assert min_validator_test2.status is False
    assert min_validator_test2.get_messages()['messages']['text']['min'] == 'it must longer than 5'


def test_max_validator():
    max_validator_test1 = MaxTestValidator({'text': '12345'})
    max_validator_test1.validate()
    assert max_validator_test1.status is True
    assert max_validator_test1.get_messages()['messages']['result'] is True
    assert max_validator_test1.get_messages()['messages']['message'] == 'OK'

    max_validator_test2 = MaxTestValidator({'text': '123456'})
    max_validator_test2.validate()
    assert max_validator_test2.status is False
    assert max_validator_test2.get_messages()['messages']['text']['max'] == 'it must be shorter than 5'


def test_unique_validator():
    unique_validator_test1 = UniqueTestValidator({'text': 'aaa'})
    unique_validator_test1.validate()
    assert unique_validator_test1.status is True
    assert unique_validator_test1.get_messages()['messages']['result'] is True
    assert unique_validator_test1.get_messages()['messages']['message'] == 'OK'

    from picopico.apps.account.models import User
    User.objects.create_superuser('123456789', '123456789')
    unique_validator_test2 = UniqueTestValidator({'text': '123456789'})
    unique_validator_test2.validate()
    assert unique_validator_test2.status is False
    assert unique_validator_test2.get_messages()['messages']['text']['unique'] == 'the 123456789 is duplicated'


def test_numberic_validator():
    data = {'text1': '123456789', 'text2': '1', 'text3': '12'}
    numberic_validator_test1 = NumbericTestValidator(data)
    numberic_validator_test1.validate()

    assert numberic_validator_test1.status is True
    assert numberic_validator_test1.get_messages()['messages']['result'] is True
    assert numberic_validator_test1.get_messages()['messages']['message'] == 'OK'
    data2 = {'text1': 'abcdef', 'text2': '12', 'text3': '123'}
    numberic_validator_test2 = NumbericTestValidator(data2)
    numberic_validator_test2.validate()

    assert numberic_validator_test2.status is False
    assert len(numberic_validator_test2.get_messages()['messages']) == 3


def test_regex_validaor():
    data1 = {'text1': '123456', 'text2': 'abcdef'}
    regex_validator_test1 = RegexTestValidator(data1)
    regex_validator_test1.validate()

    assert regex_validator_test1.status is True
    assert regex_validator_test1.get_messages()['messages']['result'] is True
    assert regex_validator_test1.get_messages()['messages']['message'] == 'OK'

    data2 = {'text1': 'abcdef', 'text2': '123456'}
    regex_validator_test2 = RegexTestValidator(data2)
    regex_validator_test2.validate()

    assert regex_validator_test2.status is False
    assert 2 == len(regex_validator_test2.get_messages()['messages'])


def test_exist_validator():
    User.objects.create_user(cellphone='123456789', password='123456789')
    data1 = {'text1': '123456789'}
    exist_validator_test1 = ExistTestValidator(data1)
    exist_validator_test1.validate()
    assert exist_validator_test1.status is True
    assert exist_validator_test1.get_messages()['messages']['result'] is True
    assert exist_validator_test1.get_messages()['messages']['message'] == 'OK'

    data2 = {'text1': '12345678910'}
    exist_validator_test2 = ExistTestValidator(data2)
    exist_validator_test2.validate()

    assert exist_validator_test2.status is False
    assert 1 == len(exist_validator_test2.get_messages()['messages'])


class ValidatorTestCase(TestCase):

    @staticmethod
    def test_alphabet_validator():
        test_alphabet_validator()

    @staticmethod
    def test_required_validator():
        test_required_validator()

    @staticmethod
    def test_min_validator():
        test_min_validator()

    @staticmethod
    def test_max_validator():
        test_max_validator()

    @staticmethod
    def test_unique_validator():
        test_unique_validator()

    @staticmethod
    def test_numberic_validator():
        test_numberic_validator()

    @staticmethod
    def test_regex_validator():
        test_regex_validaor()

    @staticmethod
    def test_exist_validator():
        test_exist_validator()

    @staticmethod
    def test_email_validator():
        test_email_validator()
