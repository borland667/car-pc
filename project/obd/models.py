# coding: utf-8
from django.db import models

# http://en.wikipedia.org/wiki/OBD-II_PIDs
class Sensor(models.Model):
    description = models.CharField(max_length='255', unique=True)
    pid = models.CharField(max_length='2', unique=True)
    unit = models.CharField(max_length='10', blank=True)

    class Meta:
        ordering = ('id', )

    def __unicode__(self):
        return self.name

    def get_command(self):
        return '01%s' % self.pid

class SensorResult(models.Model):
    sensor = models.ForeignKey(Sensor, to_field='pid')
    value = models.CharField(max_length='50')
    dc = models.DateTimeField(auto_now_add=True)