# -*- coding: utf-8 -*-

import uuid
import hashlib

from django.db import models
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class Option(models.Model):
    user = models.ForeignKey(User)
    code = models.CharField(max_length=56)
    expiry = models.DateTimeField()


class DEAMng(Option):
    user_ = None
    options = None

    class Meta:
        proxy = True

    def _get_options(self, code):
        """
        :param code: str
        :return:
        """
        try:
            self.options = Option.objects.get(code=code)
        except ObjectDoesNotExist:
            self.options = None
            raise AssertionError('Code not found')

    def _create(self, email):
        """
        :type email: str
        :return: bool
        """
        try:
            User.objects.get(email=email)
            raise AssertionError('Email already exists')
        except ObjectDoesNotExist:
            pass

        self.user_ = User.objects.create_user(
            username=uuid.uuid4(),
            email=email,
            is_staff=False,
            is_superuser=False,
            is_active=False)

        return True

    def clean_dea(self):
        """
        # :type code: str
        :return: bool
        """
        # if code:
        #     try:
        #         self._get_options(code)
        #     except AssertionError:
        #         return True

        self.options.delete()
        return True

    def set_code(self, email, expiry=1):
        """ Sign up and define code for sing in
        :type email: str
        :type expiry: int
        :return: str
        """
        try:
            self.user_ = User.objects.get(email=email)
        except ObjectDoesNotExist:
            self._create(email)

        try:
            self.options = self.user_.option_set.get()   # exception
            if self.options.code and self.options.expiry > timezone.now():
                return self.options.code
            else:
                self.clean_dea()
        except ObjectDoesNotExist:
            pass

        self.options = Option.objects.create(
            user=self.user_,
            code=hashlib.sha224(timezone.now().__str__().encode()).hexdigest(),
            expiry=timezone.now() + timezone.timedelta(hours=expiry))

        return self.options.code

    def is_valid(self, code):
        """
        :type code: str
        :return: bool
        """
        try:
            self._get_options(code)
        except AssertionError:
            return False

        if self.options.expiry > timezone.now():
            return True

        return False

    def get_user(self, email=None):
        """
        :type email: str
        :return: queryset
        """
        if email:
            return User.objects.get(email=email)
        elif self.user_:
            return self.user_
        elif self.options:
            return self.options.user
        else:
            raise AssertionError('User not found')

    def login(self, request):
        user = self.get_user()
        if user:
            if not user.is_active:
                user.is_active = True
                user.save()

            login(request, user)
            self.clean_dea()
            return
        raise AssertionError('User not defined')
