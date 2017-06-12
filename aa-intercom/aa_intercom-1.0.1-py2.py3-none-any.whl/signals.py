from aa_intercom.tasks import push_intercom_event_task


def intercom_event_push_to_intercom_post_save(sender, instance, created, **kwargs):
    push_intercom_event_task.apply_async(args=[instance.id], countdown=110)


def account_post_save(sender, instance, created, **kwargs):
    # update account in intercom
    from aa_intercom.tasks import push_account_task
    push_account_task.apply_async(args=[instance.id], countdown=10)
