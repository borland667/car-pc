# coding: utf-8
from obd.models import SensorResult
import os
from django.db import models
from core.utils import encrypt, decrypt

class OneValueModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def GetValue(cls, name, default=None, decrypt_it=False):
        instance, created = cls.objects.get_or_create(name=name, defaults={'value': default})
        value = instance.value

        if decrypt_it:
            value = decrypt(value)

        return value

    @classmethod
    def SetValue(cls, name, value, encrypt_it=False):
        if encrypt_it:
            value = encrypt(value)

        cls.objects.get_or_create(name=name)    # create if needed
        return cls.objects.filter(name=name).update(value=value)


class Status(OneValueModel):
    VIDEO_STARTED = 'VIDEO_STARTED'
    VIDEO_UPLOAD_STARTED = 'VIDEO_UPLOAD_STARTED'
    OBD_STARTED = 'OBD_STARTED'
    NAME_CHOICES = (
        (VIDEO_STARTED, 'Video capturing started'),
        (VIDEO_UPLOAD_STARTED, 'Video upload started'),
        (OBD_STARTED, 'OBD II capturing started'),
    )

    name = models.CharField(max_length=100, unique=True, choices=NAME_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)


class Settings(OneValueModel):
    SERVICE_USER_NAME = 'SERVICE_USER_NAME'
    SERVICE_USER_PASSWORD = 'SERVICE_USER_PASSWORD'
    SERVICE_CAR_NAME = 'SERVICE_CAR_NAME'
    SERVICE_CAR_PASSWORD = 'SERVICE_CAR_PASSWORD'
    NAME_CHOICES = (
        (SERVICE_USER_NAME, 'User name for internet service'),
        (SERVICE_USER_PASSWORD, 'Password for car pc Internet service'),
        (SERVICE_CAR_NAME, 'System login for transmit car data to Internet service'),
        (SERVICE_CAR_PASSWORD, 'System password for transmit car data to Internet service'),
    )
    name = models.CharField(max_length=100, unique=True, choices=NAME_CHOICES)
    value = models.CharField(max_length=255, null=True, blank=True)


class Command(models.Model):
    SYSTEM_DOWN = 'halt'
    START_VIDEO_UPLOAD = 'start video upload'
    STOP_VIDEO_UPLOAD = 'stop video upload'
    COMMAND_CHOICES = (
        (SYSTEM_DOWN, SYSTEM_DOWN),
        (START_VIDEO_UPLOAD, START_VIDEO_UPLOAD),
        (STOP_VIDEO_UPLOAD, STOP_VIDEO_UPLOAD),
    )

    command = models.CharField(max_length=15, choices=COMMAND_CHOICES, db_index=True)
    dc = models.DateTimeField(auto_now_add=True, db_index=True)
    done_time = models.DateTimeField(null=True, db_index=True)

    class Meta:
        get_latest_by = 'dc'

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
                dev_path = '/dev/%s' % file
                cls.objects.get_or_create(dev_path=dev_path, defaults={'is_uses': False})

    @classmethod
    def GetExistingDevices(cls):
        cls.InitialiseVideos()
        return [d for d in cls.objects.all() if d.exists_in_system()]


    def __unicode__(self):
        return self.get_name()

    def get_name(self):
        return self.dev_path.split('/')[-1]

    def get_resolutions(self):
        """
            return list of available resolutions for device
        """
        # FIXME: get real info from device
        return [item[0] for item in self.RESOLUTION_CHOICES]

    def exists_in_system(self):
        return os.path.exists(self.dev_path)

class UploadVideo(models.Model):
    source_path = models.CharField(max_length=255, db_index=True)
    source_size = models.BigIntegerField(db_index=True)
    destination_path = models.CharField(max_length=255)
    dc = models.DateTimeField(auto_now_add=True, db_index=True)

class SensorResultSend(models.Model):
    """
        Sending sensor result additional info
    """
    result = models.ForeignKey(SensorResult, related_name='send_data')
    send_dt = models.DateTimeField(db_index=True)

