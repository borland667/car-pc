# coding: utf-8
import os
from django.db import models


class Status(models.Model):
    VIDEO_STARTED = 'VIDEO_STARTED'
    OBD_STARTED = 'OBD_STARTED'
    NAME_CHOICES = (
        (VIDEO_STARTED, 'Video capturing started'),
        (OBD_STARTED, 'OBD II capturing started'),
    )

    name = models.CharField(max_length=100, unique=True, choices=NAME_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)

    @classmethod
    def GetValue(cls, name, default=None):
        instance, created = cls.objects.get_or_create(name=name, defaults={'value': default})
        return instance.value

    @classmethod
    def SetValue(cls, name, value):
        cls.objects.get_or_create(name=name)    # create if needed
        return cls.objects.filter(name=name).update(value=value)


class Command(models.Model):
    COMMAND_SYSTEM_DOWN = 'halt'
    COMMAND_CHOICES = (
        (COMMAND_SYSTEM_DOWN, COMMAND_SYSTEM_DOWN),
    )

    command = models.CharField(max_length=15, choices=COMMAND_CHOICES, db_index=True)
    dc = models.DateTimeField(auto_now_add=True, db_index=True)
    done_time = models.DateTimeField(null=True, db_index=True)

    def __unicode__(self):
        return '%s - %s' % (self.command, self.dc)


class VideoDevice(models.Model):
    RESOLUTION_CHOICES = (
        ('320x240', '320x240'),
        ('640x480', '640x480'),
        ('1024x768', '1024x768'),
    )
    dev_path = models.FilePathField(path='/dev/', match='video*')
    resolution = models.CharField(max_length='10', choices=RESOLUTION_CHOICES, default='640x480')
    is_uses = models.BooleanField(default=False)

    @classmethod
    def InitialiseVideos(cls):
        """
            search systems video cameras and create VideoDevice-object for each of one
        """
        for file in os.listdir("/dev"):
            if file.startswith("video"):
                cls.objects.get_or_create(dev_path=file, defaults={'is_uses': False})

    def get_name(self):
        return self.dev_path.split('/')[-1]

    def get_resolutions(self):
        """
            return list of available resolutions for device
        """
        # FIXME: get real info from device
        return [item[0] for item in self.RESOLUTION_CHOICES]