# coding: utf-8
import time

from django.conf import settings
from django.core.management.base import NoArgsCommand

from obd import obd_port
from obd import models
import core.models

class Command(NoArgsCommand):
    help = 'Capturing obd2 sensors dynamic data'


    def handle(self, *args, **options):
        while True:
            # check need to start capturing
            if self._is_started():
                self._start_capturing()

            # wait and retry check
            else:
                time.sleep(1)

    def _start_capturing(self):
        port = obd_port.OBDPort(settings.OBD_DEV_PATH)
        try:
            available_sensors = port.get_available_sensors()
            print 'OBD available sensors:', [s.name for s in available_sensors]

            print 'Start OBD2'
            while True:
                if self._is_started():
                    get_any_data = False
                    for sensor in available_sensors:
                        value = port.get_sensor_value(sensor)
                        if value:
                            get_any_data = True

                        # save result
                        pid = sensor.cmd[2:]
                        models.SensorResult.objects.create(
                            sensor_id=pid,
                            value=(value or '')
                        )
                    # if no one sensor return data, then close port for restart reading
                    if not get_any_data:
                        time.sleep(1)
                        return
                else:
                    print 'Stopped OBD2'
                    return

        finally:
            port.close()

    def _is_started(self):
        return core.models.Status.GetValue(name=core.models.Status.OBD_STARTED) == '1'

