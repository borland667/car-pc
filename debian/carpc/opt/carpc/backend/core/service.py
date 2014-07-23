# coding: utf-8
import requests
from BeautifulSoup import BeautifulSoup
from django.conf import settings

from core import models

LOGIN_URL = '/api-auth/login/'
CREATE_CAR_PC_USER = '/core/car/create/'
SENSOR_RESULT = '/core/sensor/add_result/'

class CarPcService(object):
    def __init__(self):
        self._session = requests.Session()
        self.is_logined = False

    def get_session(self):
        if not self.is_logined:
            self._login()
        return self._session

    def send_sensor_result(self, pid, value, result_dt):
        url = settings.CAR_PC_SERVICE_URL + SENSOR_RESULT
        params = {
            'sensor_pid': pid,
            'value': value,
            'result_dt': result_dt
        }
        r = self.get_session().post(url, data=params)
        self._pre_process_response('add sensor result', r)

        return r.json()

    def create_car(self, name, description):
        url = settings.CAR_PC_SERVICE_URL + CREATE_CAR_PC_USER

        params = {
            'name': name,
            'description': description,
        }

        # for creating user make special service-client and login as main user
        service = CarPcService()
        service._login(username=self._user_name(), password=self._user_password())

        r = service.get_session().post(url, data=params)
        self._pre_process_response('create car', r)

        result = r.json()
        models.Settings.SetValue(models.Settings.SERVICE_CAR_NAME, result['user_name'])
        models.Settings.SetValue(models.Settings.SERVICE_CAR_PASSWORD, result['password'], encrypt_it=True)

        # print 'status:', r.status_code
        # print 'text:', r.json()

    def _user_name(self):
        return models.Settings.GetValue(models.Settings.SERVICE_USER_NAME)
    def _user_password(self):
        return models.Settings.GetValue(models.Settings.SERVICE_USER_PASSWORD, decrypt_it=True)

    def _car_name(self):
        return models.Settings.GetValue(models.Settings.SERVICE_CAR_NAME)
    def _car_password(self):
        return models.Settings.GetValue(models.Settings.SERVICE_CAR_PASSWORD, decrypt_it=True)
    
    def _login(self, username=None, password=None):
        username = username or self._car_name()
        password = password or self._car_password()

        url = settings.CAR_PC_SERVICE_URL + LOGIN_URL
        r = self._session.get(url)

        doc = BeautifulSoup(r.text)
        csrf_input = doc.find(attrs={'name':'csrfmiddlewaretoken'})
        csrf_token = csrf_input['value']

        params = {
            'username': username,
            'password': password,
            'csrfmiddlewaretoken': csrf_token,
            'next': '/',
        }
        r = self._session.post(url, data=params)
        self._pre_process_response('login', r)

        self.is_logined = True
        # print 'status:', r.status_code
        # print 'text:', r.text

    def _pre_process_response(self, label, response):
        if response.status_code != 200:
            err_msg = '%s error!. Status code: %s. ' % (label.capitalize(), response.status_code)

            if response.status_code == 400:
                err_msg += response.json()['error']

            if response.status_code == 500:
                err_msg += '\n\n' + response.text

            raise Exception(err_msg)