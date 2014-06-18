# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Settings'
        db.create_table(u'core_settings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Settings'])


    def backwards(self, orm):
        # Deleting model 'Settings'
        db.delete_table(u'core_settings')


    models = {
        u'core.command': {
            'Meta': {'object_name': 'Command'},
            'command': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'dc': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'done_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['core']