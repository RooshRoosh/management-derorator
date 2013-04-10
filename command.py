from django.core.management.base import BaseCommand
import time

from decorator import chek_pid
from callback import callback

class Command(BaseCommand):
    @check_pid(callback)
    def handle(self, *args, **options):
        print 'Work...'
        time.sleep(10)
