# coding: utf-8
import glob
from django.http import HttpResponse
import os.path

from django.conf import settings
from wsgiref.util import FileWrapper
from core.utils import json_response, human_size


def browse(request):
    result = []

    movies = glob.glob("%s/*.mp4" % settings.MOVIE_CONVERTED)
    for movie_path in movies:
        file_name = movie_path.split('/')[-1]

        file_size = os.path.getsize(movie_path)
        human_file_size = human_size(file_size)

        result.append({
            'name': file_name,
            'size': human_file_size,
        })

    return json_response(result)

def get(request):
    file_name = request.GET['name']
    file_path = '%s/%s' % (settings.MOVIE_CONVERTED, file_name)

    # check directory is subdirectory of MUSIC_PATH
    movie_real_path = os.path.realpath(settings.MOVIE_CONVERTED)
    requested_real_path = os.path.realpath(file_path)
    if not requested_real_path.startswith(movie_real_path):
        raise Exception('Incorrect movie name "%s"' % file_name)

    movie_file = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(movie_file, content_type='video/mp4')
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    return response