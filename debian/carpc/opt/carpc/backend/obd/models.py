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
        return self.description

    def get_command(self):
        return '01%s' % self.pid

class SensorResult(models.Model):
    sensor = models.ForeignKey(Sensor, to_field='pid', related_name='results', db_index=True)
    value = models.CharField(max_length='50', db_index=True)
    dc = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        get_latest_by = 'dc'

    def __unicode__(self):
        return '%s - %s' % (self.sensor_id, self.value)
