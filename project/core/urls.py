# coding: utf-8
from django.conf.urls import patterns, include, url

urlpatterns = patterns('core.views',
    url(r'^$', 'index.index'),

)