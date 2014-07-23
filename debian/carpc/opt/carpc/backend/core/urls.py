# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
    # url(r'^$', 'index.index'),

    url(r'^video/start_capture/$', 'video.start_capture'),
    url(r'^video/stop_capture/$', 'video.stop_capture'),
    url(r'^video/start_upload/$', 'video.start_upload'),
    url(r'^video/stop_upload/$', 'video.stop_upload'),
    url(r'^video/devices/$', 'video.devices'),
    url(r'^video/devices/(\d+)/resolution/$', 'video.set_device_resolution'),
    url(r'^video/devices/(\d+)/uses/$', 'video.set_device_uses'),

    url(r'^obd/start_capture/$', 'obd_control.start_capture'),
    url(r'^obd/stop_capture/$', 'obd_control.stop_capture'),
    url(r'^obd/last_results/$', 'obd_control.last_results'),

    url(r'^status/system_status/$', 'status.system_status'),

    url(r'^settings/car_pc_service/$', 'settings.car_pc_service'),

    url(r'^system_control/halt/$', 'system_control.halt'),

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

    url(r'^movie/browse/$', 'movie.browse'),
    url(r'^movie/get/$', 'movie.get'),

)