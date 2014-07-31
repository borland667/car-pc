# coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils import json_response, audio_cards_list
from core import models


def list_cards(request):
    result = {}
    result['cards'] = audio_cards_list()
    return json_response(result)

def get_current(request):
    card_name = models.Settings.GetValue(models.Settings.AUDIO_CARD)
    return json_response(card_name)

@csrf_exempt
@require_POST
def set_current(request):
    card_name = request.POST['card_name']

    models.Settings.SetValue(models.Settings.AUDIO_CARD, card_name)

    return json_response('Ok')