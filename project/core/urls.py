# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index.index'),

    url(r'^video/start_capture/$', 'video.start_capture'),
    url(r'^video/stop_capture/$', 'video.stop_capture'),

    url(r'^status/system_status/$', 'status.system_status'),

)