# coding: utf-8
import time
import datetime
import subprocess
import os
import signal

from django.core.management.base import NoArgsCommand
from django.conf import settings

from core import models


class Command(NoArgsCommand):
    help = 'Video capturing command (must be started in background with django-server)'

    def handle(self, *args, **options):
        while True:
            # check need to tart capturing
            if self._is_started():
                return_code = self._start_capturing()

                if self._is_started() and return_code != 0:
                    # try kill other for restarting
                    subprocess.check_call('killall streamer', shell=True)
                    time.sleep(1)

            # wait and retry check
            else:
                time.sleep(0.1)

    def _start_capturing(self):

        video_path = self._get_path()
        command = 'streamer -q -c /dev/video0 -f jpeg -t 00:05:00 -s 640x480 -o %s' % video_path
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        print 'Started'
        while p.poll() is None:
            if self._is_started():
                time.sleep(0.1)
            else:
                os.killpg(p.pid, signal.SIGTERM)
                print 'Stopped'
                return
        print 'End: %s' % p.returncode
        return p.returncode


    def _is_started(self):
        return models.Status.GetValue(name=models.Status.VIDEO_STARTED) == '1'

    def _curr_dt(self):
        return datetime.datetime.now().isoformat()[:19]

    def _get_path(self):

        # video directory
        if not os.path.exists(settings.VIDEO_PATH):
            os.makedirs(settings.VIDEO_PATH)
        # full path to file
        output_path = os.path.join(settings.VIDEO_PATH, self._curr_dt()) + '.avi'
        return output_path