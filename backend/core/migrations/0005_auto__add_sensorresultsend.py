# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SensorResultSend'
        db.create_table(u'core_sensorresultsend', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result', self.gf('django.db.models.fields.related.ForeignKey')(related_name='send_data', to=orm['obd.SensorResult'])),
            ('send_dt', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
        ))
        db.send_create_signal(u'core', ['SensorResultSend'])


    def backwards(self, orm):
        # Deleting model 'SensorResultSend'
        db.delete_table(u'core_sensorresultsend')


    models = {
        u'core.command': {
            'Meta': {'object_name': 'Command'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'dc': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'done_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.sensorresultsend': {
            'Meta': {'object_name': 'SensorResultSend'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'send_data'", 'to': u"orm['obd.SensorResult']"}),
            'send_dt': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'})
        },
        u'core.settings': {
            'Meta': {'object_name': 'Settings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.status': {
            'Meta': {'object_name': 'Status'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.videodevice': {
            'Meta': {'object_name': 'VideoDevice'},
            'dev_path': ('django.db.models.fields.FilePathField', [], {'path': "'/dev/'", 'max_length': '100', 'match': "'video*'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_uses': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resolution': ('django.db.models.fields.CharField', [], {'default': "'640x480'", 'max_length': "'10'"})
        },
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
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'results'", 'to_field': "'pid'", 'to': u"orm['obd.Sensor']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'db_index': 'True'})
        }
    }

    complete_apps = ['core']