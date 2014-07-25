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
    help = 'Movie convertor command (must be started in background with django-server)'

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        while True:
            file_path = self._get_unconverted()
            if file_path:
                self._convert(file_path)

            # wait and retry check
            time.sleep(1)

    def _get_unconverted(self):
        for file_name in listdir(settings.MOVIE_INPUT):
            file_path = os.path.join(settings.MOVIE_INPUT, file_name)
            if not os.path.isfile(file_path):
                continue

            # check converting history
            file_size = os.path.getsize(file_path)
            if models.ConvertingVideo.objects.filter(source_path=file_path, source_size=file_size).exists():
                continue

            return file_path

    def _convert(self, file_path):
        move_name = os.path.splitext(os.path.basename(file_path))[0] + '.mp4'
        move_path = os.path.join(settings.MOVIE_CONVERTED, move_name)
        print 'Converting "%s" to "%s"... ' % (file_path, move_path),

        command = 'avconv -y -i %s -strict experimental  -loglevel warning %s' % (
            file_path,
            move_path
        )
        result = os.system(command)
        if result:
            raise Exception('Error of converting.')

        file_size = os.path.getsize(file_path)
        models.ConvertingVideo.objects.create(
            source_path=file_path,
            source_size=file_size,
            destination_path=move_path,
        )
        print 'Ok.'