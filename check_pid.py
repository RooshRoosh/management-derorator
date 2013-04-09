from django.db import models
from django.core.management.base import BaseCommand

class PidFlag(models.Model):
    command = models.TextField()
    flag = models.BooleanField()

def check_pid(function):
    def wrapper(self, *args, **options):
        command = self.__class__.__name__
        try:
            pid = PidFlag.objects.get(command = command)
        except:
            pid = PidFlag.objects.create(command = command,
                                         flag = False)
        if not pid.flag:
            raise Exception('Already work...')
        else:
            pid.flag = True
            pid.save()
            fucntion(self, *args, **options)
            pid.flag = False
            pid.save()
    return wrapper


class MyCommand(BaseCommad):
    @check_pid
    def handle(self, *args, **options):
        pass
