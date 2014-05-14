# coding: utf-8
from core.utils import json_response
from django.views.decorators.csrf import csrf_exempt

from core import models
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def start_capture(request):
    if 'start' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '1')
        return json_response("Started")


@require_POST
@csrf_exempt
def stop_capture(request):
    if 'stop' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '0')
        return json_response("Stopped")
