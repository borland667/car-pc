# coding: utf-8
import urllib
import urllib2
import base64
import xml.etree.ElementTree as ET
from core.utils import json_response

from django.conf import settings

from core import models
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def browse(request):
    url = settings.VLC_HTTP + '/requests/browse.xml'
    params = {
        'dir': request.GET.get('dir', settings.MUSIC_PATH),
    }
    xml_tree = _get_xml(url, params)

    result = []
    for el in xml_tree.iterfind('element'):
        result.append({
            'name': el.attrib.get('name'),
            'type': el.attrib.get('type'),
            'path': el.attrib.get('path'),
            'uri': el.attrib.get('uri'),
        })

    return json_response(result)


def playlist(request):
    url = settings.VLC_HTTP + '/requests/playlist.xml'
    xml_tree = _get_xml(url)

    result = []
    items = _find_element(xml_tree, 'leaf')
    for el in items:
        duration_human = None
        if el.attrib.get('duration'):
            duration = el.attrib['duration']
            duration_human = '%s:%02d' % (
                int(duration) / 60,
                int(duration) % 60
            )

        result.append({
            'id': el.attrib.get('id'),
            'name': el.attrib.get('name'),
            'duration_sec': el.attrib.get('duration'),
            'duration_human': duration_human,
            'uri': el.attrib.get('uri'),
            'current': el.attrib.get('current'),
        })

    return json_response(result)


def status(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    xml_tree = _get_xml(url)
    result = {
        'time': xml_tree.find('time').text,
        'length': xml_tree.find('length').text,
        'state': xml_tree.find('state').text,
        'position': xml_tree.find('position').text,
        'title': xml_tree.find(".//info[@name='title']").text,
        'album': xml_tree.find(".//info[@name='album']").text,
        'artist': xml_tree.find(".//info[@name='artist']").text,
        'filename': xml_tree.find(".//info[@name='filename']").text,
    }

    for info in ['title', 'album', 'artist', 'filename']:
        el = xml_tree.find(".//info[@name='%s']" % info)
        if el:
            result[info] = el.text

    return json_response(result)


@require_POST
@csrf_exempt
def in_play(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    input_path = request.POST['input']
    params = {'command': 'in_play', 'input': input_path}
    _get_xml(url, params)
    return json_response('Ok')



@require_POST
@csrf_exempt
def play(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    id = request.POST['id']
    params = {'command': 'pl_play', 'id': id}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def in_enqueue(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    input_path = request.POST['input']
    params = {'command': 'in_enqueue', 'input': input_path}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def pause(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_pause'}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def stop(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_stop'}
    _get_xml(url, params)
    return json_response('Ok')

@require_POST
@csrf_exempt
def next(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_next'}
    _get_xml(url, params)
    return json_response('Ok')

@require_POST
@csrf_exempt
def previous(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_previous'}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def empty(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_empty'}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def delete(request, id):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_delete', 'id': id}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def random(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_random'}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def loop(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_loop'}
    _get_xml(url, params)
    return json_response('Ok')


@require_POST
@csrf_exempt
def repeat(request):
    url = settings.VLC_HTTP + '/requests/status.xml'
    params = {'command': 'pl_repeat'}
    _get_xml(url, params)
    return json_response('Ok')


def _get_xml(base_url, params=None):
    if params:
        for k, v in params.items():
            params[k] = v.encode('utf-8')
        params_encoded = urllib.urlencode(params).replace('+', '%20')
        url = '%s?%s' % (base_url, params_encoded)
    else:
        url = base_url

    auth_encoded = base64.encodestring('%s:%s' % (settings.VLC_LOGIN, settings.VLC_PASSWORD)).replace('\n', '')

    request = urllib2.Request(url)
    request.add_header("Authorization", "Basic %s" % auth_encoded)
    response = urllib2.urlopen(request)

    xml_text = response.read()
    return ET.fromstring(xml_text)


def _find_element(xml_element, tag_name):
    elements = []
    for el in xml_element:
        if el.tag == tag_name:
            elements.append(el)
        elif len(el):
            inner_elements = _find_element(el, tag_name)
            elements.extend(inner_elements)
    return elements
