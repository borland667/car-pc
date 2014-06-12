# coding: utf-8
import time
import datetime
import subprocess
import os
import signal

from django.core.management.base import NoArgsCommand
from django.conf import settings
import picamera

from core import models


class Command(NoArgsCommand):
    help = 'Video capturing command (must be started in background with django-server)'

    def handle(self, *args, **options):
        while True:
            # check need to start capturing
            if self._is_started():
                self._start_capturing()

            # wait and retry check
            else:
                time.sleep(1)

    def _start_capturing(self):
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            video_path = self._get_path()
            camera.start_recording(video_path)
            print 'Start video'
            while True:
                if self._is_started():
                    camera.wait_recording(1)
                else:
                    camera.stop_recording()
                    print 'Stopped video'
                    return


    def _is_started(self):
        return models.Status.GetValue(name=models.Status.VIDEO_STARTED) == '1'

    def _curr_dt(self):
        return datetime.datetime.now().isoformat()[:19]

    def _get_path(self):

        # video directory
        if not os.path.exists(settings.VIDEO_PATH):
            os.makedirs(settings.VIDEO_PATH)
        # full path to file
        output_path = os.path.join(settings.VIDEO_PATH, self._curr_dt()) + '.h264'
        return output_path