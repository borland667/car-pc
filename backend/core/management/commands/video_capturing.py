# coding: utf-8
from optparse import make_option
import time
import datetime
import subprocess
import os
import signal

from django.core.management.base import BaseCommand
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = 'Video capturing command (must be started in background with django-server)'

    option_list = BaseCommand.option_list + (
        make_option('--device', help='Path for video device. For example, /dev/video0. '),
    )

    def handle(self, *args, **options):
        device = options.get('device')
        if device:
            if not os.path.isfile(device):
                raise Exception('Device "%s" not found' % device)
        # TODO: make multiprocess start of all system video devices
        else:
            print 'No device!'
            return

        while True:
            # check need to tart capturing
            if self._is_started():
                return_code = self._start_capturing(device)

                if self._is_started() and return_code != 0:
                    # try kill other for restarting
                    subprocess.check_call('killall streamer', shell=True)
                    time.sleep(1)

            # wait and retry check
            else:
                time.sleep(0.1)

    def _start_capturing(self, device):
        video_device, created = models.VideoDevice.objects.get_or_create(dev_path=device, defaults={'is_uses': True})

        command = 'streamer -q -c %s -f jpeg -t 00:05:00 -s %s -o %s' % (
            video_device.dev_path,
            video_device.resolution,
            self._get_path(video_device.get_name())
        )

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

    def _get_path(self, device_name):

        # video directory
        if not os.path.exists(settings.VIDEO_PATH):
            os.makedirs(settings.VIDEO_PATH)
        # full path to file
        file_name = '%s%s.avi' % (device_name, self._curr_dt())
        output_path = os.path.join(settings.VIDEO_PATH, file_name)
        return output_path