# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index.index'),

    url(r'^video/start_capture/$', 'video.start_capture'),
    url(r'^video/stop_capture/$', 'video.stop_capture'),

)