# coding: utf-8
import time
import datetime
import subprocess
import os
import signal

from django.core.management.base import NoArgsCommand
from django.conf import settings

import obd.models
from core import models
from core import service


class Command(NoArgsCommand):
    help = 'Sending statistic data to car-pc-service'

    def handle(self, *args, **options):
        srv = service.CarPcService()

        while True:
            for result in obd.models.SensorResult.objects.filter(send_data__send_dt__isnull=True):
                # print 'Sending %s...' % result,
                send_result = srv.send_sensor_result(
                    pid=result.sensor_id,
                    value=result.value,
                    result_dt=result.dc,
                )
                models.SensorResultSend.objects.create(
                    result=result,
                    send_dt=datetime.datetime.now()
                )
                # print send_result
            time.sleep(5)
