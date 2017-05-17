from __future__ import unicode_literals

import logging

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from nodeconductor.core import tasks as core_tasks, utils as core_utils
from nodeconductor.quotas import exceptions as quotas_exceptions
from nodeconductor.structure import (models as structure_models, tasks as structure_tasks,
                                     SupportedServices)

from . import models, serializers


logger = logging.getLogger(__name__)


class RuntimeStateException(Exception):
    pass


class PollRuntimeStateTask(core_tasks.Task):
    max_retries = 300
    default_retry_delay = 5

    @classmethod
    def get_description(cls, instance, backend_pull_method, *args, **kwargs):
        return 'Poll instance "%s" with method "%s"' % (instance, backend_pull_method)

    def get_backend(self, instance):
        return instance.get_backend()

    def execute(self, instance, backend_pull_method, success_state, erred_state):
        backend = self.get_backend(instance)
        getattr(backend, backend_pull_method)(instance)
        instance.refresh_from_db()
        if instance.runtime_state not in (success_state, erred_state):
            self.retry()
        elif instance.runtime_state == erred_state:
            raise RuntimeStateException(
                '%s %s (PK: %s) runtime state become erred: %s' % (
                    instance.__class__.__name__, instance, instance.pk, erred_state))
        return instance


class SetInstanceOKTask(core_tasks.StateTransitionTask):
    """ Additionally mark or related floating IPs as free """

    def pre_execute(self, instance):
        self.kwargs['state_transition'] = 'set_ok'
        self.kwargs['action'] = ''
        self.kwargs['action_details'] = {}
        super(SetInstanceOKTask, self).pre_execute(instance)

    def execute(self, instance, *args, **kwargs):
        super(SetInstanceOKTask, self).execute(instance)
        instance.floating_ips.update(is_booked=False)


class SetInstanceErredTask(core_tasks.ErrorStateTransitionTask):
    """ Mark instance as erred and delete resources that were not created. """

    def execute(self, instance):
        super(SetInstanceErredTask, self).execute(instance)

        # delete volumes if they were not created on backend,
        # mark as erred if creation was started, but not ended,
        # leave as is, if they are OK.
        for volume in instance.volumes.all():
            if volume.state == models.Volume.States.CREATION_SCHEDULED:
                volume.delete()
            elif volume.state == models.Volume.States.OK:
                pass
            else:
                volume.set_erred()
                volume.save(update_fields=['state'])

        # set instance floating IPs as free, delete not created ones.
        instance.floating_ips.filter(backend_id='').delete()
        instance.floating_ips.update(is_booked=False)


class SetBackupErredTask(core_tasks.ErrorStateTransitionTask):
    """ Mark DR backup and all related resources that are not in state OK as Erred """

    def execute(self, backup):
        super(SetBackupErredTask, self).execute(backup)
        for snapshot in backup.snapshots.all():
            # If snapshot creation was not started - delete it from NC DB.
            if snapshot.state == models.Snapshot.States.CREATION_SCHEDULED:
                snapshot.decrease_backend_quotas_usage()
                snapshot.delete()
            else:
                snapshot.set_erred()
                snapshot.save(update_fields=['state'])

        # Deactivate schedule if its backup become erred.
        schedule = backup.backup_schedule
        if schedule:
            schedule.error_message = 'Failed to execute backup schedule for %s. Error: %s' % (
                backup.instance, backup.error_message)
            schedule.is_active = False
            schedule.save()


class ForceDeleteBackupTask(core_tasks.DeletionTask):

    def execute(self, backup):
        backup.snapshots.all().delete()
        super(ForceDeleteBackupTask, self).execute(backup)


class SetBackupRestorationErredTask(core_tasks.ErrorStateTransitionTask):
    """ Mark backup restoration instance as erred and
        delete volume records that have not been created on backend.
    """

    def execute(self, backup_restoration):
        instance = backup_restoration.instance
        super(SetBackupRestorationErredTask, self).execute(instance)
        # delete volumes if they were not created on backend,
        # mark as erred if creation was started, but not ended,
        # leave as is, if they are OK.
        for volume in instance.volumes.all():
            if volume.state == models.Volume.States.CREATION_SCHEDULED:
                volume.delete()
            elif volume.state == models.Volume.States.OK:
                pass
            else:
                volume.set_erred()
                volume.save(update_fields=['state'])


class VolumeExtendErredTask(core_tasks.ErrorStateTransitionTask):
    """ Mark volume and its instance as erred on fail """

    def execute(self, volume):
        super(VolumeExtendErredTask, self).execute(volume)
        if volume.instance is not None:
            super(VolumeExtendErredTask, self).execute(volume.instance)


class BaseScheduleTask(core_tasks.BackgroundTask):
    model = NotImplemented

    def is_equal(self, other_task):
        return self.name == other_task.get('name')

    def run(self):
        schedules = self.model.objects.filter(is_active=True, next_trigger_at__lt=timezone.now())
        for schedule in schedules:
            kept_until = None
            if schedule.retention_time:
                kept_until = timezone.now() + timezone.timedelta(days=schedule.retention_time)

            try:
                with transaction.atomic():
                    schedule.call_count += 1
                    schedule.save()
                    resource = self._create_resource(schedule, kept_until=kept_until)
            except quotas_exceptions.QuotaValidationError as e:
                message = 'Failed to schedule "%s" creation. Error: %s' % (self.model.__name__, e)
                logger.exception(
                    'Resource schedule (PK: %s), (Name: %s) execution failed. %s' % (schedule.pk,
                                                                                     schedule.name,
                                                                                     message))
                schedule.is_active = False
                schedule.error_message = message
                schedule.save()
            else:
                executor = self._get_create_executor()
                executor.execute(resource)
                schedule.update_next_trigger_at()
                schedule.save()

    def _create_resource(self, schedule, kept_until):
        raise NotImplementedError()

    def _get_create_executor(self):
        raise NotImplementedError()


class ScheduleBackups(BaseScheduleTask):
    name = 'openstack_tenant.ScheduleBackups'
    model = models.BackupSchedule

    def _create_resource(self, schedule, kept_until):
        backup = models.Backup.objects.create(
            name='Backup#%s of %s' % (schedule.call_count, schedule.instance.name),
            description='Scheduled backup of instance "%s"' % schedule.instance,
            service_project_link=schedule.instance.service_project_link,
            instance=schedule.instance,
            backup_schedule=schedule,
            metadata=serializers.BackupSerializer.get_backup_metadata(schedule.instance),
            kept_until=kept_until,
        )
        serializers.BackupSerializer.create_backup_snapshots(backup)
        return backup

    def _get_create_executor(self):
        from . import executors
        return executors.BackupCreateExecutor


class DeleteExpiredBackups(core_tasks.BackgroundTask):
    name = 'openstack_tenant.DeleteExpiredBackups'

    def is_equal(self, other_task):
        return self.name == other_task.get('name')

    def run(self):
        from . import executors
        for backup in models.Backup.objects.filter(kept_until__lt=timezone.now(), state=models.Backup.States.OK):
            executors.BackupDeleteExecutor.execute(backup)


class ScheduleSnapshots(BaseScheduleTask):
    name = 'openstack_tenant.ScheduleSnapshots'
    model = models.SnapshotSchedule

    def _create_resource(self, schedule, kept_until):
        snapshot = models.Snapshot.objects.create(
            name='Snapshot#%s of %s' % (schedule.call_count, schedule.source_volume.name),
            description='Scheduled snapshot of volume "%s"' % schedule.source_volume,
            service_project_link=schedule.source_volume.service_project_link,
            source_volume=schedule.source_volume,
            snapshot_schedule=schedule,
            size=schedule.source_volume.size,
            metadata=serializers.SnapshotSerializer.get_snapshot_metadata(schedule.source_volume),
            kept_until=kept_until,
        )
        snapshot.increase_backend_quotas_usage()
        return snapshot

    def _get_create_executor(self):
        from . import executors
        return executors.SnapshotCreateExecutor


class DeleteExpiredSnapshots(core_tasks.BackgroundTask):
    name = 'openstack_tenant.DeleteExpiredSnapshots'

    def is_equal(self, other_task):
        return self.name == other_task.get('name')

    def run(self):
        from . import executors
        for snapshot in models.Snapshot.objects.filter(kept_until__lt=timezone.now(), state=models.Snapshot.States.OK):
            executors.SnapshotDeleteExecutor.execute(snapshot)


class SetErredStuckResources(core_tasks.BackgroundTask):
    name = 'openstack_tenant.SetErredStuckResources'

    def is_equal(self, other_task):
        return self.name == other_task.get('name')

    def run(self):
        for model in (models.Instance, models.Volume, models.Snapshot):
            cutoff = timezone.now() - timedelta(minutes=30)
            for resource in model.objects.filter(modified__lt=cutoff,
                                                 state=structure_models.NewResource.States.CREATING):
                resource.set_erred()
                resource.error_message = 'Provisioning is timed out.'
                resource.save(update_fields=['state', 'error_message'])
                logger.warning('Switching resource %s to erred state, '
                               'because provisioning is timed out.',
                               core_utils.serialize_instance(resource))


class LimitedPerTypeThrottleMixin(object):

    def get_limit(self, resource):
        nc_settings = getattr(settings, 'NODECONDUCTOR_OPENSTACK', {})
        limit_per_type = nc_settings.get('MAX_CONCURRENT_PROVISION', {})
        model_name = SupportedServices.get_name_for_model(resource)
        return limit_per_type.get(model_name, super(LimitedPerTypeThrottleMixin, self).get_limit(resource))


class ThrottleProvisionTask(LimitedPerTypeThrottleMixin, structure_tasks.ThrottleProvisionTask):
    pass


class ThrottleProvisionStateTask(LimitedPerTypeThrottleMixin, structure_tasks.ThrottleProvisionStateTask):
    pass
