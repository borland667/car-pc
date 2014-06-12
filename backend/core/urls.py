# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index.index'),

    url(r'^video/start_capture/$', 'video.start_capture'),
    url(r'^video/stop_capture/$', 'video.stop_capture'),

    url(r'^obd/start_capture/$', 'obd.start_capture'),
    url(r'^obd/stop_capture/$', 'obd.stop_capture'),

    url(r'^status/system_status/$', 'status.system_status'),

    url(r'^player/browse/$', 'player.browse'),
    url(r'^player/playlist/$', 'player.playlist'),
    url(r'^player/status/$', 'player.status'),
    url(r'^player/in_play/$', 'player.in_play'),
    url(r'^player/play/$', 'player.play'),
    url(r'^player/in_enqueue/$', 'player.in_enqueue'),
    url(r'^player/pause/$', 'player.pause'),
    url(r'^player/stop/$', 'player.stop'),
    url(r'^player/next/$', 'player.next'),
    url(r'^player/previous/$', 'player.previous'),
    url(r'^player/empty/$', 'player.empty'),
    url(r'^player/delete/(\d+)/$', 'player.delete'),
    url(r'^player/random/$', 'player.random'),
    url(r'^player/loop/$', 'player.loop'),
    url(r'^player/repeat/$', 'player.repeat'),
    url(r'^player/volume/$', 'player.volume'),
    url(r'^player/seek/$', 'player.seek'),

)