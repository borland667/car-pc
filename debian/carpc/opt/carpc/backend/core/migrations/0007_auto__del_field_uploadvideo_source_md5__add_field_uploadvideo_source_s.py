# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UploadVideo.source_md5'
        db.delete_column(u'core_uploadvideo', 'source_md5')

        # Adding field 'UploadVideo.source_size'
        db.add_column(u'core_uploadvideo', 'source_size',
                      self.gf('django.db.models.fields.BigIntegerField')(default=0, db_index=True),
                      keep_default=False)

        # Adding index on 'UploadVideo', fields ['source_path']
        db.create_index(u'core_uploadvideo', ['source_path'])


    def backwards(self, orm):
        # Removing index on 'UploadVideo', fields ['source_path']
        db.delete_index(u'core_uploadvideo', ['source_path'])


        # User chose to not deal with backwards NULL issues for 'UploadVideo.source_md5'
        raise RuntimeError("Cannot reverse this migration. 'UploadVideo.source_md5' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UploadVideo.source_md5'
        db.add_column(u'core_uploadvideo', 'source_md5',
                      self.gf('django.db.models.fields.CharField')(max_length=100),
                      keep_default=False)

        # Deleting field 'UploadVideo.source_size'
        db.delete_column(u'core_uploadvideo', 'source_size')


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
        u'core.uploadvideo': {
            'Meta': {'object_name': 'UploadVideo'},
            'dc': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'destination_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'source_size': ('django.db.models.fields.BigIntegerField', [], {'db_index': 'True'})
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