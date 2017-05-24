# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import uuid

from django.utils.crypto import salted_hmac


class UserModelMixin(object):

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        Compatibility with authn login
        """
        key_salt = (
            'letmein.models.User.get_session_auth_hash'
        )

        return salted_hmac(key_salt, self.secret).hexdigest()

    @property
    def pk(self):
        return self.id_user

    @property
    def is_staff(self):
        return True

    def has_module_perms(self, lbl):
        return True

    def has_perm(self, lbl):
        return True

    def save(self, update_fields=[]):
        pass

    class Serialization:
        def __init__(self):
            pass

        class pk:
            def __init__(self):
                pass

            @staticmethod
            def to_python(key):
                return uuid.UUID(key)

            @staticmethod
            def value_to_string(value):
                return str(value.pk)
