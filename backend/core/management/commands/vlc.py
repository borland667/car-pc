# coding: utf-8
import subprocess
import time
import signal
from core.utils import audio_cards_list
import os.path

from django.core.management.base import BaseCommand
from django.conf import settings

from core import models


class Command(BaseCommand):
    help = 'VLC support (must be started in background with django-server)'

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        while True:
            self._start_vlc()

    def _start_vlc(self):
        card_param = ''
        self.working_card_index = self._get_card_index()
        if self.working_card_index:
            card_param = 'PULSE_SINK=%s' % self.working_card_index

        http_passwd_param = ''
        if settings.VLC_PASSWORD:
            http_passwd_param = '--http-password %s' % settings.VLC_PASSWORD

        command = '%s %s -I http %s' % (
            card_param,
            settings.VLC_BIN,
            http_passwd_param,
        )

        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
        print 'Started vlc'
        try:
            while p.poll() is None:
                if self._no_changes():
                    time.sleep(1)
                else:
                    break
        finally:
            os.killpg(p.pid, signal.SIGTERM)
            print 'Stopped vlc'

        print 'End: %s' % p.returncode
        return p.returncode


    def _no_changes(self):
        if self.working_card_index == self._get_card_index():
            return True
        else:
            return False


    def _get_card_index(self):
        card_name = models.Settings.GetValue(models.Settings.AUDIO_CARD)
        if card_name:
            try:
                card = [card for card in audio_cards_list() if card['name'] == card_name][0]
                return card['index']
            except Exception:
                return None

