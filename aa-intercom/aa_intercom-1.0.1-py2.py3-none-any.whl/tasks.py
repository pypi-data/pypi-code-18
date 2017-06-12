# -*- coding: utf-8 -*-
from datetime import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.timezone import make_aware
from intercom import IntercomError, MultipleMatchingUsersError
from intercom.client import Client

from aa_intercom.celery import app
from aa_intercom.utils import upload_intercom_user, upload_not_registered_user_data

intercom = Client(personal_access_token=settings.INTERCOM_API_ACCESS_TOKEN)

LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes


@app.task(ignore_result=True)
def push_account_task(obj_id):
    """
    Async: push_account_task.delay(Account.id)
    """
    lock_id = "%s-push-account-%s" % (settings.ENV_PREFIX, obj_id)
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)  # noqa: E731
    release_lock = lambda: cache.delete(lock_id)  # noqa: E731
    if acquire_lock():
        UserModel = get_user_model()
        try:
            upload_intercom_user(obj_id)
        except UserModel.DoesNotExist:
            #  seems like account was removed before it was pushed
            release_lock()

        release_lock()


@app.task(ignore_result=True)
def push_intercom_event_task(obj_id):
    """
    Async: push_intercom_event_task.delay(event.id)
    """
    lock_id = "%s-push-intercom_event-%s" % (settings.ENV_PREFIX, obj_id)
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)  # noqa: E731
    release_lock = lambda: cache.delete(lock_id)  # noqa: E731

    if acquire_lock():
        from aa_intercom.models import IntercomEvent
        try:
            instance = IntercomEvent.objects.get(pk=obj_id)
            if instance.is_sent:
                return

            data = instance.get_intercom_data()
            try:
                if instance.user:
                    upload_intercom_user(instance.user.pk)
                else:
                    upload_not_registered_user_data({"email": data["metadata"]["email"]})
                if not getattr(settings, "SKIP_INTERCOM", False):
                    intercom.events.create(**data)
                    IntercomEvent.objects.filter(pk=obj_id).update(
                        is_sent=True
                    )
            except IntercomError:
                IntercomEvent.objects.filter(pk=obj_id).update(
                    is_sent=False
                )
                release_lock()
                raise  # FIXME - to check when errror happens

        except IntercomEvent.DoesNotExist:
            release_lock()
            raise
        release_lock()


@app.task(ignore_result=True)
def push_account_last_seen_task(obj_id):
    """
    Async: push_account_last_seen_task.apply_async(args=[Account.id], countdown=100)
    """
    lock_id = "%s-push-account-last-seen-%s" % (settings.ENV_PREFIX, obj_id)  # noqa: E731
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)  # noqa: E731
    # lock is not released on purpose. We want 5 mins cache for subsequent calls.
    # release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        intercom_user = False
        UserModel = get_user_model()
        try:
            instance = UserModel.objects.get(pk=obj_id)
            data = {
                "user_id": instance.intercom_id,
                "email": instance.email,
                "name": instance.get_full_name(),
                "last_request_at": instance.last_login.strftime("%s") if instance.last_login else "",
            }
            if not getattr(settings, "SKIP_INTERCOM", False):
                intercom_user = intercom.users.create(**data)

            if intercom_user:
                UserModel.objects.filter(pk=obj_id).update(
                    intercom_last_api_response=intercom_user.__dict__,
                    intercom_api_response_timestamp=make_aware(datetime.now(), pytz.UTC)
                )
        except UserModel.DoesNotExist:
            raise


@app.task(ignore_result=True)
def push_not_registered_user_data_task(data):
    """
    Async: push_not_registered_user_data_task.apply_async(args=[data], countdown=100)
    """
    lock_id = "%s-push-not-registered-user-data-task-%s" % (settings.ENV_PREFIX, data["email"])
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)  # noqa: E731
    release_lock = lambda: cache.delete(lock_id)  # noqa: E731

    if acquire_lock():
        try:
            upload_not_registered_user_data(data)
        except (KeyError, NotImplementedError, MultipleMatchingUsersError):
            release_lock()
            raise
        release_lock()
