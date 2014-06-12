# coding: utf-8
import urllib
import urllib2
import base64
import xml.etree.ElementTree as ET
import os.path

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from core.utils import json_response


def browse(request):
    url = settings.VLC_HTTP + '/requests/browse.xml'

    dir = request.GET.get('dir', settings.MUSIC_PATH)

    # check directory is subdirectory of MUSIC_PATH
    music_real_path = os.path.realpath(settings.MUSIC_PATH)
    requested_real_path = os.path.realpath(dir)
    if not requested_real_path.startswith(music_real_path):
        dir = settings.MUSIC_PATH

    params = {
        'dir': dir,
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
            duration_human = _humanize_time(duration)

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
        'time': _get_node_text(xml_tree, 'time'),
        'length': _get_node_text(xml_tree, 'length'),
        'state': _get_node_text(xml_tree, 'state'),
        'position': _get_node_text(xml_tree, 'position'),
        'title': _get_node_text(xml_tree, ".//info[@name='title']"),
        'album': _get_node_text(xml_tree, ".//info[@name='album']"),
        'artist': _get_node_text(xml_tree, ".//info[@name='artist']"),
        'filename': _get_node_text(xml_tree, ".//info[@name='filename']"),
    }

    if result.get('time'):
        result['time_human'] = _humanize_time(result['time'])

    if result.get('time') and result.get('length'):
        secs_for_end = int(result['length']) - int(result['time'])
        result['time_for_end_human'] = _humanize_time(secs_for_end)

    for info in ['title', 'album', 'artist', 'filename', 'track_number']:
        result[info] = _get_node_text(xml_tree, ".//info[@name='%s']" % info)

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

def _get_node_text(xml_tree, selector):
    result = None
    el = xml_tree.find(selector)
    if el is not None:
        result = el.text
    return result


def _find_element(xml_element, tag_name):
    elements = []
    for el in xml_element:
        if el.tag == tag_name:
            elements.append(el)
        elif len(el):
            inner_elements = _find_element(el, tag_name)
            elements.extend(inner_elements)
    return elements

def _humanize_time(secs):
    human_time = '%s:%02d' % (
        int(secs) / 60,
        int(secs) % 60
    )
    return human_time