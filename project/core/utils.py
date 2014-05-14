# coding: utf-8
import json
from django.http import HttpResponse


def json_response(data):
    data_json = json.dumps(data)
    return HttpResponse(data_json, content_type='application/json')