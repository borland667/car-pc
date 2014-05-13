# coding: utf-8
import json
from django.http import HttpResponse

from core import models

def system_status(request):
    status = {}

    for name, label in models.Status.NAME_CHOICES:
        status[name] = models.Status.GetValue(name)

    status_json = json.dumps(status)
    return HttpResponse(status_json, content_type='application/json')