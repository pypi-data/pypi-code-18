# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.timezone import make_aware, now
from intercom import errors
from intercom.client import Client

intercom = Client(personal_access_token=settings.INTERCOM_API_ACCESS_TOKEN)


def upload_intercom_user(obj_id):
    """Creates or updates single user account on intercom"""
    UserModel = get_user_model()
    intercom_user = False
    instance = UserModel.objects.get(pk=obj_id)
    data = instance.get_intercom_data()

    if not getattr(settings, "SKIP_INTERCOM", False):
        try:
            intercom_user = intercom.users.create(**data)
        except errors.ServiceUnavailableError:
            pass

    if intercom_user:
        UserModel.objects.filter(pk=obj_id).update(
            intercom_last_api_response=intercom_user.to_dict(),
            intercom_api_response_timestamp=make_aware(datetime.now(), pytz.UTC)
        )


def upload_not_registered_user_data(data):
    """
        Upload user data to intercom, actually any data passed
        data: Dict
        Required:
        "email"
    """
    if type(data) != dict:
        raise NotImplementedError("Incorrect data type")

    if not data.get("email"):
        raise KeyError("user_id as user.intercom_id or email is required")

    if not getattr(settings, "SKIP_INTERCOM", False):
        intercom_data = {
            "email": data.get("email"),
            "name": data.get("name"),
            "last_request_at": now().strftime("%s"),
        }
        del(data["email"])
        if data.get("name"):
            del(data["name"])
        if data:
            intercom_data["custom_attributes"] = data
        try:
            intercom.users.create(**intercom_data)
        except errors.ServiceUnavailableError:
            pass
