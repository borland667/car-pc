# coding: utf-8
from core.utils import json_response
from django.views.decorators.csrf import csrf_exempt

from core import models
from django.views.decorators.http import require_POST


@require_POST
@csrf_exempt
def start_capture(request):
    if 'start' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '1')
        return json_response("Started")


@require_POST
@csrf_exempt
def stop_capture(request):
    if 'stop' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_STARTED, '0')
        return json_response("Stopped")


@require_POST
@csrf_exempt
def start_upload(request):
    if 'start' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_UPLOAD_STARTED, '1')
        return json_response("Started")


@require_POST
@csrf_exempt
def stop_upload(request):
    if 'stop' in request.POST:
        models.Status.SetValue(models.Status.VIDEO_UPLOAD_STARTED, '0')
        return json_response("Stopped")


def devices(request):
    """
        list of video devices in system
    """
    result = []
    for device in models.VideoDevice.GetExistingDevices():
        result.append({
            'id': device.id,
            'dev_path': device.dev_path,
            'name': device.get_name(),
            'resolution': device.resolution,
            'available_resolutions': device.get_resolutions(),
            'is_uses': device.is_uses,
        })
    return json_response(result)


@require_POST
@csrf_exempt
def set_device_uses(request, id):
    is_uses = int(request.POST['is_uses'])
    models.VideoDevice.objects.filter(id=id).update(is_uses=is_uses)
    return json_response("Ok")

@require_POST
@csrf_exempt
def set_device_resolution(request, id):
    models.VideoDevice.objects.filter(id=id).update(resolution=request.POST['resolution'])
    return json_response("Ok")
