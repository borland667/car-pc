# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sensor'
        db.create_table(u'obd_sensor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length='255')),
            ('pid', self.gf('django.db.models.fields.CharField')(unique=True, max_length='2')),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length='10', blank=True)),
        ))
        db.send_create_signal(u'obd', ['Sensor'])

        # Adding model 'SensorResult'
        db.create_table(u'obd_sensorresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['obd.Sensor'], to_field='pid')),
            ('value', self.gf('django.db.models.fields.CharField')(max_length='50')),
            ('dc', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'obd', ['SensorResult'])


    def backwards(self, orm):
        # Deleting model 'Sensor'
        db.delete_table(u'obd_sensor')

        # Deleting model 'SensorResult'
        db.delete_table(u'obd_sensorresult')


    models = {
        u'obd.sensor': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Sensor'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'255'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': "'2'"}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': "'10'", 'blank': 'True'})
        },
        u'obd.sensorresult': {
            'Meta': {'object_name': 'SensorResult'},
            'dc': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['obd.Sensor']", 'to_field': "'pid'"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': "'50'"})
        }
    }

    complete_apps = ['obd']