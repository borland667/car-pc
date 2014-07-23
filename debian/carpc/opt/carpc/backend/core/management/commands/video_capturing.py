# coding: utf-8
from optparse import make_option
import time
import datetime
import subprocess
import threading
from django.core.management import call_command
import os
import signal
import sys

from django.core.management.base import BaseCommand
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = 'Video capturing command (must be started in background with django-server)'

    option_list = BaseCommand.option_list + (
        make_option('--device', help='Path for video device. For example, /dev/video0. '),
    )

    def handle(self, *args, **options):
        device_path = options.get('device')

        # Event from main thread about ending main thread
        quit_event = options.get('quit_event')

        # if device specified
        if device_path:
            if not os.path.exists(device_path):
                raise Exception('Device "%s" not found' % device_path)

            while True:
                # if main thread is exit
                if quit_event.isSet():
                    return

                # check need to start capturing
                if self._is_started(device_path):
                    return_code = self._start_capturing(device_path, quit_event)

                    if self._is_started(device_path) and return_code != 0:
                        # try kill other for restarting
                        subprocess.check_call('killall streamer', shell=True)
                        time.sleep(1)

                # wait and retry check
                else:
                    time.sleep(0.1)

        # if not device not specified, start for all exists devices own video_capturing command
        else:
            # thread for each used device
            threads = {}
            quit_event = threading.Event()
            try:
                while True:
                    if self._is_started():
                        for device in models.VideoDevice.objects.filter(is_uses=True):
                            device_tread = threads.get(device.id)
                            if not (device_tread and device_tread.is_alive()):
                                t = threading.Thread(
                                    target=call_command,
                                    args=('video_capturing',),
                                    kwargs={'device': device.dev_path, 'quit_event':quit_event}
                                )
                                t.start()
                                threads[device.id] = t

                                print 'Start thread for device ', device.get_name()

                    time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                quit_event.set()
                sys.exit()

    def _start_capturing(self, device_path, quit_event):
        video_device, created = models.VideoDevice.objects.get_or_create(dev_path=device_path, defaults={'is_uses': True})
        if not video_device.is_uses:
            return

        video_device_qs = models.VideoDevice.objects.filter(
            id=video_device.id,
            is_uses=video_device.is_uses,
            resolution=video_device.resolution,
        )

        # 5 minutes - standard video length
        video_length = '5'
        # for upload video mode make video shorter - 1 minute
        if models.Status.GetValue(models.Status.VIDEO_UPLOAD_STARTED) == '1':
            video_length = '1'

        command = 'streamer -q -c %s -f jpeg -t 00:0%s:00 -s %s -o %s' % (
            video_device.dev_path,
            video_length,
            video_device.resolution,
            self._get_path(video_device.get_name())
        )

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        print 'Started'
        while p.poll() is None:
            if self._is_started() and video_device_qs.exists() and not quit_event.isSet():
                time.sleep(0.1)
            else:
                os.killpg(p.pid, signal.SIGTERM)
                print 'Stopped'
                break
        print 'End: %s' % p.returncode
        return p.returncode


    def _is_started(self, device_path=None):
        capturing = models.Status.GetValue(name=models.Status.VIDEO_STARTED) == '1'

        if capturing and device_path:
            capturing = models.VideoDevice.objects.filter(dev_path=device_path, is_uses=True).exists()

        return capturing

    def _curr_dt(self):
        return datetime.datetime.now().isoformat()[:19]

    def _get_path(self, device_name):

        # video directory
        if not os.path.exists(settings.VIDEO_PATH):
            os.makedirs(settings.VIDEO_PATH)
        # full path to file
        file_name = '%s_%s.avi' % (device_name, self._curr_dt())
        output_path = os.path.join(settings.VIDEO_PATH, file_name)
        return output_path