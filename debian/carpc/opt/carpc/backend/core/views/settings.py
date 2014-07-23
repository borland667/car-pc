# coding: utf-8
from core.utils import json_response
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core import models

@csrf_exempt
@require_POST
def car_pc_service(request):
    user_name = request.POST['user_name']
    password = request.POST['password']

    models.Settings.SetValue(models.Settings.SERVICE_USER_NAME, user_name)
    models.Settings.SetValue(models.Settings.SERVICE_USER_PASSWORD, password, encrypt_it=True)

    return json_response('Ok')