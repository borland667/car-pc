# coding: utf-8
import time
import datetime
import os
from django.core.management.base import NoArgsCommand
from core import models


class Command(NoArgsCommand):
    help = 'Monitoring core.Commands for system and process their'

    def handle(self, *args, **options):
        while True:
            # process halt commands
            halt_commands_qs = models.Command.objects.filter(
                command=models.Command.COMMAND_SYSTEM_DOWN,
                done_time__isnull=True
            )
            if halt_commands_qs.exists():
                halt_commands_qs.update(done_time=datetime.datetime.now())
                command = 'halt -p'
                result = os.system(command)
                if result != 0:
                    raise Exception('Error of processing command "%s"' % command)

            time.sleep(1)
