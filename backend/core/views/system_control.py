# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils import json_response
from core import models


@require_POST
@csrf_exempt
def halt(request):
    if 'halt' in request.POST:
        models.Command.objects.create(
            command=models.Command.COMMAND_SYSTEM_DOWN
        )
        return json_response("Ok")
