# author: Shane Yu  date: April 8, 2017
from django.core.management.base import BaseCommand, CommandError
from PMIofKCM import PMI

class Command(BaseCommand):
    help = 'use this for build pmi of kcm!'
    
    def handle(self, *args, **options):
        p = PMI()
        p.build()
        self.stdout.write(self.style.SUCCESS("測試：臺南市的pmi"))
        self.stdout.write(self.style.SUCCESS(p.get("臺南市", 10)))
        self.stdout.write(self.style.SUCCESS('build kem model success!!!'))