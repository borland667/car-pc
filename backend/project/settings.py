# coding: utf-8
from project.settings_default import *

LANGUAGE_CODE = 'ru'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'car_pc',
#         'USER': 'car_pc',
#         'HOST': 'localhost',
#         'PORT': None,
#         'PASSWORD': '123',
#         'CHARSET': 'utf8',
#         'TEST_CHARSET': 'utf8',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'car_pc.db'),
    }
}

MUSIC_PATH = '/Users/telminov/Music/'