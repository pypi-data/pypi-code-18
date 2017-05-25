# -*- coding: utf-8 -*-
from aa_intercom.celery import app
from aa_intercom.utils import upload_intercom_user, upload_not_registered_user_data
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils.timezone import make_aware
from django.utils.translation import ugettext_lazy as _
from intercom import IntercomError, MultipleMatchingUsersError
from intercom.client import Client

import calendar
import pytz

intercom = Client(personal_access_token=settings.INTERCOM_API_ACCESS_TOKEN)

LOCK_EXPIRE = 60 * 5  # Lock expires in 5 minutes


@app.task(ignore_result=True)
def push_account_task(obj_id):
    """
    from nutriom.intercom.tasks import push_account_task

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
    from nutriom.intercom.tasks import push_account_task

    Async: push_intercom_event_task.delay(event.id)
    """
    lock_id = "%s-push-intercom_event-%s" % (settings.ENV_PREFIX, obj_id)
    acquire_lock = lambda: cache.add(lock_id, "true", LOCK_EXPIRE)  # noqa: E731
    release_lock = lambda: cache.delete(lock_id)  # noqa: E731

    if acquire_lock():
        from .models import IntercomEvent
        try:
            instance = IntercomEvent.objects.get(pk=obj_id)
            if instance.is_sent:
                return
            if instance.type == IntercomEvent.TYPE_EXAMPLE_EVENT:
                data = {
                    "event_name": instance.get_type_display(),  # event type
                    "created_at": calendar.timegm(instance.created.utctimetuple()),  # date
                    "user_id": instance.user.intercom_id,  # user id
                    "metadata": {
                        "text_content": instance.text_content,
                        # anything more you want
                    }
                }

            elif instance.type in [
                IntercomEvent.TYPE_GENERIC,
                # TODO: fine tune per project
            ]:
                data = {
                    "event_name": instance.get_type_display(),  # event type
                    "created_at": calendar.timegm(instance.created.utctimetuple()),  # date
                    "user_id": instance.user.intercom_id,  # creator id
                    "metadata": {
                        "text_content": instance.text_content,  # text, depending on the object
                        # type of content (topic, session, what to do, etc)
                        "type": instance.content_type.name if instance.content_type else "",
                        "id": instance.object_id if instance.object_id else "",  # id of object from type
                    }
                }
            else:
                release_lock()
                raise AttributeError(_("There is no action for this event type: ") + instance.type)
            try:
                if instance.user:
                    upload_intercom_user(instance.user.pk)
                else:
                    upload_not_registered_user_data({"email": data["email"]})
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
    from demo.intercom.tasks import push_account_last_seen_task

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
    from nutriom.intercom.tasks import push_not_registered_user_data_task

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
