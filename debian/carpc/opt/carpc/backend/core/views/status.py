# coding: utf-8
from core.utils import json_response
from core import models

def system_status(request):
    status = {}

    for name, label in models.Status.NAME_CHOICES:
        status[name] = models.Status.GetValue(name)

    return json_response(status)
