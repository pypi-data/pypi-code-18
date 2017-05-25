from aa_intercom.tasks import push_intercom_event_task
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save


def intercom_event_push_to_intercom_post_save(sender, instance, created, **kwargs):
    push_intercom_event_task.apply_async(args=[instance.id], countdown=110)


def account_post_save(sender, instance, created, **kwargs):
    # update account in intercom
    from aa_intercom.tasks import push_account_task
    push_account_task.apply_async(args=[instance.id], countdown=10)


post_save.connect(account_post_save, sender=get_user_model())
