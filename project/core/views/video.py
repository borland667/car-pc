# coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from core import models


@csrf_exempt
def start_capture(request):
    if 'start' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '1')
        return HttpResponse('"Started"', content_type='application/json')


@csrf_exempt
def stop_capture(request):
    if 'stop' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '0')
        return HttpResponse('"Stopped"', content_type='application/json')
