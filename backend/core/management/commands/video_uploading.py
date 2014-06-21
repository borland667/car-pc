# coding: utf-8
import time
import datetime
from os import listdir
import os.path
import hashlib
import pytz.reference
import shutil

from django.core.management.base import BaseCommand
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = 'Video uploading command (must be started in background with django-server)'

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        while True:
            # check need to start uploading
            if self._is_started():
                print 'Check uploading...'
                self._start_uploading()
                print 'All copied for uploading'

            # wait and retry check
            time.sleep(1)


    def _start_uploading(self):
        # search last start command
        start_command_qs = models.Command.objects.filter(command=models.Command.START_VIDEO_UPLOAD)
        if not start_command_qs.exists():
            return
        start_command = start_command_qs.latest()

        # should not be exists stop command
        stop_command_qs = models.Command.objects.filter(
            command=models.Command.STOP_VIDEO_UPLOAD,
            id__gt=start_command.id
        )
        if stop_command_qs.exists():
            return

        # 5 minutes early then start command (with a reserve)
        start_time = start_command.dc - datetime.timedelta(minutes=5)

        # search files for upload
        video_files = []
        for filename in listdir(settings.VIDEO_PATH):
            file_path = os.path.join(settings.VIDEO_PATH, filename)
            if not os.path.isfile(file_path):
                continue

            # check time
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path), tz=pytz.reference.LocalTimezone())
            if start_time > file_time:
                continue

            # check upload history by md5
            md5sum = hashlib.md5(file_path).hexdigest()
            if models.UploadVideo.objects.filter(source_path=file_path, source_md5=md5sum).exists():
                continue

            video_files.append([filename, md5sum])

        # copy to upload directory
        for filename, md5sum in video_files:
            src_path = os.path.join(settings.VIDEO_PATH, filename)
            dst_path = os.path.join(settings.VIDEO_UPLOAD_PATH, filename)

            shutil.copyfile(src_path, dst_path)

            models.UploadVideo.objects.create(
                source_path=src_path,
                source_md5=md5sum,
                destination_path=dst_path,
            )
            print 'Copied %s' % filename


    def _is_started(self):
        uploading = models.Status.GetValue(name=models.Status.VIDEO_UPLOAD_STARTED) == '1'
        return uploading
