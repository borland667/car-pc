# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'SensorResult', fields ['dc']
        db.create_index(u'obd_sensorresult', ['dc'])


    def backwards(self, orm):
        # Removing index on 'SensorResult', fields ['dc']
        db.delete_index(u'obd_sensorresult', ['dc'])


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
            'dc': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['obd.Sensor']", 'to_field': "'pid'"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': "'50'"})
        }
    }

    complete_apps = ['obd']