# coding: utf-8
from collections import OrderedDict
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils import json_response
from core import models

@require_POST
@csrf_exempt
def start_capture(request):
    if 'start' in request.POST:
        models.Status.SetValue(models.Status.OBD_STARTED, '1')
        return json_response("Started")


@require_POST
@csrf_exempt
def stop_capture(request):
    if 'stop' in request.POST:
        models.Status.SetValue(models.Status.OBD_STARTED, '0')
        return json_response("Stopped")


def last_results(request):
    import obd.models

    results = []
    for sensor in obd.models.Sensor.objects.all():
        if sensor.results.exclude(value__in=('', 'NO DATA')).exists():
            latest = sensor.results.exclude(value__in=('', 'NO DATA')).latest()
            results.append({
                'description': sensor.description,
                'pid': sensor.pid,
                'unit': sensor.unit,
                'value': latest.value,
                'date_time': latest.dc,
            })

    return json_response(results)