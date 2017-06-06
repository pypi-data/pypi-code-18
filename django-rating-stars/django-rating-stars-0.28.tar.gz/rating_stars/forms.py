# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .models import Rating


class UpdateRatingForm(forms.Form):
    rating = forms.IntegerField(widget=forms.HiddenInput())
    content_type = forms.CharField(widget=forms.HiddenInput())
    object_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean(self):
        cleaned_data = super(UpdateRatingForm, self).clean()
        user_id = cleaned_data.get('user_id')
        ctype_id = cleaned_data.get('content_type')
        obj_id = cleaned_data.get('object_id')

        try:
            user_id = int(user_id)
        except ValueError:
            user_id = -1

        try:
            ctype_id = int(ctype_id)
        except ValueError:
            ctype_id = -1

        try:
            obj_id = int(obj_id)
        except ValueError:
            obj_id = -1

        if not ContentType.objects.filter(id=ctype_id).exists():
            raise forms.ValidationError(
                message=_("Dont change data")
            )
        else:
            ctype = ContentType.objects.get(id=ctype_id)
            if not ctype.model_class().objects.get(id=obj_id):
                raise forms.ValidationError(
                    message=_("Dont change data")
                )

        if not User.objects.filter(id=user_id).exists():
            raise forms.ValidationError(
                message=_("Only authorized user can vote")
            )

        user = User.objects.get(id=user_id)
        if Rating.objects.filter(
            user=user,
            content_type=ctype,
            object_id=obj_id
        ).exists():
            raise forms.ValidationError(
                message=_("You've already voted")
            )
        return cleaned_data
