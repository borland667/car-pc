# coding: utf-8
import re
import base64
import hashlib
import json
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
    output = """

    index: 0
        name: <alsa_card.pci-0000_01_00.1>
        driver: <module-alsa-card.c>
        owner module: 5
        properties:
            alsa.card = "1"
            alsa.card_name = "HDA NVidia"
            alsa.long_card_name = "HDA NVidia at 0xd3000000 irq 17"
            alsa.driver_name = "snd_hda_intel"
            device.bus_path = "pci-0000:01:00.1"
            sysfs.path = "/devices/pci0000:00/0000:00:01.0/0000:01:00.1/sound/card1"
            device.bus = "pci"
            device.vendor.id = "10de"
            device.vendor.name = "NVIDIA Corporation"
            device.product.id = "0be3"
            device.product.name = "High Definition Audio Controller"
            device.string = "1"
            device.description = "High Definition Audio Controller"
            module-udev-detect.discovered = "1"
            device.icon_name = "audio-card-pci"
        profiles:
            output:hdmi-stereo: Digital Stereo (HDMI) Output (priority 5400, available: unknown)
            output:hdmi-surround: Digital Surround 5.1 (HDMI) Output (priority 300, available: unknown)
            output:hdmi-stereo-extra1: Digital Stereo (HDMI) Output (priority 5200, available: unknown)
            output:hdmi-surround-extra1: Digital Surround 5.1 (HDMI) Output (priority 100, available: unknown)
            output:hdmi-stereo-extra2: Digital Stereo (HDMI) Output (priority 5200, available: unknown)
            output:hdmi-surround-extra2: Digital Surround 5.1 (HDMI) Output (priority 100, available: unknown)
            output:hdmi-stereo-extra3: Digital Stereo (HDMI) Output (priority 5200, available: unknown)
            output:hdmi-surround-extra3: Digital Surround 5.1 (HDMI) Output (priority 100, available: unknown)
            off: Off (priority 0, available: unknown)
        active profile: <output:hdmi-stereo>
        sinks:
            alsa_output.pci-0000_01_00.1.hdmi-stereo/#0: High Definition Audio Controller Digital Stereo (HDMI)
        sources:
            alsa_output.pci-0000_01_00.1.hdmi-stereo.monitor/#0: Monitor of High Definition Audio Controller Digital Stereo (HDMI)
        ports:
            hdmi-output-0: HDMI / DisplayPort (priority 5900, latency offset 0 usec, available: no)
                properties:
                    device.icon_name = "video-display"
            hdmi-output-1: HDMI / DisplayPort 2 (priority 5800, latency offset 0 usec, available: no)
                properties:
                    device.icon_name = "video-display"
            hdmi-output-2: HDMI / DisplayPort 3 (priority 5700, latency offset 0 usec, available: no)
                properties:
                    device.icon_name = "video-display"
            hdmi-output-3: HDMI / DisplayPort 4 (priority 5600, latency offset 0 usec, available: no)
                properties:
                    device.icon_name = "video-display"

    index: 1
        name: <alsa_card.pci-0000_00_1b.0>
        driver: <module-alsa-card.c>
        owner module: 6
        properties:
            alsa.card = "0"
            alsa.card_name = "HDA Intel MID"
            alsa.long_card_name = "HDA Intel MID at 0xdb100000 irq 45"
            alsa.driver_name = "snd_hda_intel"
            device.bus_path = "pci-0000:00:1b.0"
            sysfs.path = "/devices/pci0000:00/0000:00:1b.0/sound/card0"
            device.bus = "pci"
            device.vendor.id = "8086"
            device.vendor.name = "Intel Corporation"
            device.product.id = "3b56"
            device.product.name = "5 Series/3400 Series Chipset High Definition Audio"
            device.form_factor = "internal"
            device.string = "0"
            device.description = "Built-in Audio"
            module-udev-detect.discovered = "1"
            device.icon_name = "audio-card-pci"
        profiles:
            input:analog-stereo: Analog Stereo Input (priority 60, available: unknown)
            output:analog-stereo: Analog Stereo Output (priority 6000, available: unknown)
            output:analog-stereo+input:analog-stereo: Analog Stereo Duplex (priority 6060, available: unknown)
            off: Off (priority 0, available: unknown)
        active profile: <output:analog-stereo+input:analog-stereo>
        sinks:
            alsa_output.pci-0000_00_1b.0.analog-stereo/#1: Built-in Audio Analog Stereo
        sources:
            alsa_output.pci-0000_00_1b.0.analog-stereo.monitor/#1: Monitor of Built-in Audio Analog Stereo
            alsa_input.pci-0000_00_1b.0.analog-stereo/#2: Built-in Audio Analog Stereo
        ports:
            analog-input: Analog Input (priority 10000, latency offset 0 usec, available: unknown)
                properties:

            analog-output: Analog Output (priority 9900, latency offset 0 usec, available: unknown)
                properties:

    >>> """

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