# coding: utf-8
from django.contrib import admin
from obd import models

class SensorAdmin(admin.ModelAdmin):
    list_display = ('description', 'pid', 'unit',)
admin.site.register(models.Sensor, SensorAdmin)