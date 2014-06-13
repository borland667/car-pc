# coding: utf-8
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

def json_response(data):
    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    response = HttpResponse(data_json, content_type='application/json')
    # response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8001'
    # response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    # response['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
    # response['Access-Control-Allow-Credentials'] = 'true'
    return response