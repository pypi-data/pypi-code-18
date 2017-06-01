# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from jpstring import validators


class BaseValidator(object):
    message = '正しい値を入力して下さい。'
    code = 'invalid'

    def __init__(self, message=None):
        if message:
            self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        if not self.validate(cleaned):
            raise ValidationError(
                self.message,
                code=self.code,
                params=self.get_error_context(value, cleaned),
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and (self.message == other.message)
            and (self.code == other.code)
        )

    def clean(self, value):
        return value

    def validate(self, value):
        raise NotImplementedError()

    def get_error_context(self, value, cleaned_value):
        return {'value': value, 'show_value': cleaned_value}


@deconstructible
class HiraganaValidator(BaseValidator):
    message = 'すべてひらがなで入力して下さい。'

    def validate(self, value):
        return validators.is_hiragana(value)


@deconstructible
class KatakanaValidator(BaseValidator):
    message = 'すべてカタカナで入力して下さい。'

    def validate(self, value):
        return validators.is_katakana(value)


@deconstructible
class NumericValidator(BaseValidator):
    message = 'すべて数字文字で入力して下さい。'

    def validate(self, value):
        return validators.is_numeric(value)


@deconstructible
class ZipcodeValidator(BaseValidator):
    message = '正しくない郵便番号です。'

    def __init__(self, split=False, message=None):
        self.split = split
        super(ZipcodeValidator, self).__init__(message)

    def __eq__(self, other):
        return super(ZipcodeValidator, self).__eq__(other) and (
            self.split == other.split
        )

    def validate(self, value):
        return validators.is_zipcode(value, split=self.split)


@deconstructible
class PhoneNumberValidator(BaseValidator):
    message = '正しくない電話番号です。'

    def __init__(self, split=False, message=None):
        self.split = split
        super(PhoneNumberValidator, self).__init__(message)

    def __eq__(self, other):
        return super(PhoneNumberValidator, self).__eq__(other) and (
            self.split == other.split
        )

    def validate(self, value):
        return validators.is_phone_number(value, split=self.split)


@deconstructible
class MobileNumberValidator(BaseValidator):
    message = '正しくない携帯電話番号です。'

    def __init__(self, split=False, message=None):
        self.split = split
        super(MobileNumberValidator, self).__init__(message)

    def __eq__(self, other):
        return super(MobileNumberValidator, self).__eq__(other) and (
            self.split == other.split
        )

    def validate(self, value):
        return validators.is_mobile_number(value, split=self.split)


@deconstructible
class MaxLengthValidator(BaseValidator):
    message = '%(max)s 文字以上である必要があります。'
    code = 'max_length'

    def __init__(self, max, message=None, **kwargs):
        self.max = max
        self.options = kwargs
        super(MaxLengthValidator, self).__init__(message)

    def __eq__(self, other):
        return super(MaxLengthValidator, self).__eq__(other) and (
            self.max == other.max
        )

    def validate(self, value):
        return validators.max_length(value, self.max, **self.options)

    def get_error_context(self, *args, **kwargs):
        context = super(MaxLengthValidator, self).get_error_context(
            *args,
            **kwargs
        )
        context['max'] = self.max
        context.update(self.options)
        return context


@deconstructible
class MinLengthValidator(BaseValidator):
    message = '%(min)s 文字以下である必要があります。'
    code = 'min_length'

    def __init__(self, min, message=None, **kwargs):
        self.min = min
        self.options = kwargs
        super(MinLengthValidator, self).__init__(message)

    def __eq__(self, other):
        return super(MinLengthValidator, self).__eq__(other) and (
            self.min == other.min
        )

    def validate(self, value):
        return validators.min_length(value, self.min, **self.options)

    def get_error_context(self, *args, **kwargs):
        context = super(MinLengthValidator, self).get_error_context(
            *args,
            **kwargs
        )
        context['min'] = self.min
        context.update(self.options)
        return context


@deconstructible
class BetweenValidator(BaseValidator):
    message = '%(min)s 文字以上かつ、%(max)s 文字以下である必要があります。'
    code = 'between'

    def __init__(self, min, max, message=None, **kwargs):
        self.min = min
        self.max = max
        self.options = kwargs
        super(BetweenValidator, self).__init__(message)

    def __eq__(self, other):
        return super(MinLengthValidator, self).__eq__(other) and (
            self.min == other.min
            and self.max == other.max
        )

    def validate(self, value):
        return validators.between(value, self.min, self.max, **self.options)

    def get_error_context(self, *args, **kwargs):
        context = super(BetweenValidator, self).get_error_context(
            *args,
            **kwargs
        )
        context['min'] = self.min
        context['max'] = self.max
        context.update(self.options)
        return context
