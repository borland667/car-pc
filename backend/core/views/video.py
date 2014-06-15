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


def devices(request):
    """
        list of video devices in system
    """
    result = []
    models.VideoDevice.InitialiseVideos()
    for device in models.VideoDevice.objects.all():
        result.append({
            'id': device.id,
            'dev_path': device.dev_path,
            'name': device.get_name(),
            'resolution': device.resolution,
            'is_uses': device.is_uses,
        })
    return json_response(result)


@require_POST
@csrf_exempt
def edit_device(request, id):
    device = models.VideoDevice.objects.get(id=id)

    if request.POST.get('resolution'):
        device.resolution = request.POST['resolution']

    if request.POST.get('is_uses'):
        device.is_uses = int(request.POST['is_uses'])

    device.save()
    return json_response("Ok")

