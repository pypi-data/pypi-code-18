from django.core.management.base import BaseCommand, CommandError
from YaBackup.backup import YaBackup


class Command(BaseCommand):
    help = 'Run YaBackup'

    def handle(self, *args, **options):
        job = YaBackup()
        job.run_backups()
        self.stdout.write(self.style.SUCCESS('Successfully made backups'))