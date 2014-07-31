# coding: utf-8
import re
import base64
import hashlib
import json
import subprocess
import tempfile
from Crypto.Cipher import AES
from django.conf import settings
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

def json_response(data):
    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    return HttpResponse(data_json, content_type='application/json')

def encrypt(raw):
    cipher = AES.new(_hash_key(), AES.MODE_ECB)
    padded = _pad(raw)
    encrypted = cipher.encrypt(padded)
    encoded = base64.b64encode(encrypted)
    return encoded

def decrypt(encoded):
    cipher = AES.new(_hash_key(), AES.MODE_ECB)
    encrypted = base64.b64decode(encoded)
    padded = cipher.decrypt(encrypted)
    raw = _unpad(padded)
    return raw

def human_size(num):
    num = int(num)
    for x in ['bytes','KB','MB','GB','TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def audio_cards_list():
    output = ''
    try:
        with tempfile.TemporaryFile() as tempf:
            proc = subprocess.Popen(['pacmd list-cards'], stdout=tempf)
            proc.wait()
            tempf.seek(0)
            print tempf.read()
    except Exception:
        pass

    cards = []

    for card_info in output.split('index: '):
        card_info = card_info.strip()
        if not card_info:
            continue

        # card index
        mo = re.search(r'^(\d+)', card_info)
        if mo:
            card_index = mo.group(1)
        else:
            continue

        # card name
        mo = re.search(r'name: (.+)\n', card_info)
        if mo:
            card_name = mo.group(1)
        else:
            continue

        cards.append({
            'index': card_index,
            'name': card_name,
        })

    return cards


def _hash_key(size=16):
    hashed_key = hashlib.sha1(settings.SECRET_KEY)
    return hashed_key.digest()[:size]

def _pad(text, size=16):
    return text + (size - len(text) % size) * chr(size - len(text) % size)
def _unpad(text):
    return text[0:-ord(text[-1])]