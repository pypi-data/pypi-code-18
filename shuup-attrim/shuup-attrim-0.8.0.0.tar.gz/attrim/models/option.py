from typing import List

from django.db import models
from parler.managers import TranslationQueryset, TranslationManager
from parler.models import TranslatableModel
from parler.models import TranslatedFields
from parler.utils.context import switch_language

from attrim.models.attribute import Attribute
from attrim.models.cls import Class
from attrim.models.type import Type
from attrim.trans_str import OptionValue, TransStr


class OptionQueryset(TranslationQueryset):
    def create(
        self,
        cls: Class,
        value: OptionValue = None,
        order: int = None,
        attributes: List[Attribute] = None,
        **kwargs
    ) -> 'Option':
        """
        Allows to use the virtual `value` property in the `create` method, like:
            Option.objects.create(value='{value}')
        in place of the real fields:
            Option.objects.create(_value_trans_str='{value}')
        """
        option = Option(cls=cls, order=order, **kwargs)
        if value is not None:
            option.set_value(value)
        option.save(force_insert=True, using=self.db)
        if attributes is not None:
            option.attributes.set(attributes)
        return option


class OptionManager(TranslationManager):
    def get_queryset(self) -> OptionQueryset:
        return OptionQueryset(self.model, using=self.db)


# TODO: cls and value must be unique together
class Option(TranslatableModel):
    attributes = models.ManyToManyField(
        Attribute,
        related_name='options',
        related_query_name='option',
        blank=True,
    )
    cls = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name='options',
        related_query_name='option',
    )
    order = models.PositiveSmallIntegerField(null=True, blank=True)

    _value_decimal = models.DecimalField(
        max_digits=36,
        decimal_places=9,
        null=True, blank=True,
    )
    _value_str = models.TextField(blank=True)
    translations = TranslatedFields(
        _value_trans_str=models.TextField(blank=True)
    )

    objects = OptionManager()

    class Meta:
        ordering = ['order']

    def get_value(self) -> OptionValue:
        if self.cls.type == Type.INT:
            # noinspection PyTypeChecker
            return int(self._value_decimal)
        elif self.cls.type == Type.DECIMAL:
            return self._value_decimal
        elif self.cls.type == Type.STR:
            return self._value_str
        elif self.cls.type == Type.TRANS_STR:
            # noinspection PyUnresolvedReferences
            return self._value_trans_str

    def set_value(self, value: OptionValue):
        if self.cls.type == Type.INT or self.cls.type == Type.DECIMAL:
            self._value_decimal = value
        elif self.cls.type == Type.STR:
            self._value_str = value
        elif self.cls.type == Type.TRANS_STR:
            if type(value) is str:
                self._value_trans_str = value
            if type(value) is TransStr:
                # noinspection PyTypeChecker
                for lang_code, value_translated in value:
                    with switch_language(self, lang_code):
                        self._value_trans_str = value_translated

    def __str__(self) -> str:
        return self.get_value()
