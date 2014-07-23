# coding: utf-8
# http://www.obdtester.com/elm-usb-commands

import serial
import obd_sensors
import time

# def decrypt_dtc_code(code):
#     """
#         Returns the 5-digit DTC code from hex encoding
#     """
#     dtc = []
#     current = code
#     for i in range(0,3):
#         if len(current) < 4:
#             raise "Tried to decode bad DTC: %s" % code
#
#         tc = obd_sensors.hex_to_int(current[0])  # type code
#         tc >>= 2
#         if tc == 0:
#             t = "P"
#         elif tc == 1:
#             t = "C"
#         elif tc == 2:
#             t = "B"
#         elif tc == 3:
#             t = "U"
#         else:
#             raise tc
#
#         dig1 = str(obd_sensors.hex_to_int(current[0]) & 3)
#         dig2 = str(obd_sensors.hex_to_int(current[1]))
#         dig3 = str(obd_sensors.hex_to_int(current[2]))
#         dig4 = str(obd_sensors.hex_to_int(current[3]))
#         dtc.append(t + dig1 + dig2 + dig3 + dig4)
#         current = current[4:]
#     return dtc


class OBDPortInitialiseException(Exception): pass

class OBDPort(object):
    """
        OBDPort abstracts all communication with OBD-II device.
    """
    def __init__(self, dev_path, time_out=2, baud_rate=38400):
        self.port = None
        self.elm_version = "Unknown"
        self._opened = False

        self._init_port(dev_path, time_out, baud_rate)

        self._send_command("0100")
        ready = self._get_result()
        print 'ready: ', ready

        return

    def close(self):
        if self.is_open():
            self._send_command("atz")
            self.port.close()

        self.port = None
        self.elm_version = "Unknown"
        self._opened = False

    def is_open(self):
        return self._opened

    def get_available_sensors(self):
        # Supported PIDs
        s = obd_sensors.SENSORS[0]
        value = self.get_sensor_value(s)

        if value:
            support_data = dict([(sensor_index, int(v)) for sensor_index, v in enumerate(value)])
        else:
            support_data = {}

        support_sensors = []
        for sensor_index, sensor in enumerate(obd_sensors.SENSORS):
            if support_data.get(sensor_index):
                support_sensors.append(sensor)
        return support_sensors

    def get_sensor_value(self, sensor):
        cmd = sensor.cmd
        self._send_command(cmd)
        result = self._get_result()

        if result:
            data = self._interpret_result(result)
            if result not in ('NODATA', 'NO DATA'):
                try:
                    return sensor.value(data)
                except Exception:
                    return None

        return None


    def _init_port(self, dev_path, time_out, baud_rate):
        try:
            # try to connect to OBD device
            self.port = serial.Serial(dev_path, baud_rate, timeout=time_out)
            self._opened = True

            # Performs device reset and returns ELM-USB identification
            self._send_command("atz")
            self.elm_version = self._get_result(have_echo=True)
            print 'ELM version: ', self.elm_version

            # echo off
            self._send_command("ate0")
            self._get_result()

            search_counter = 0
            while self._is_searching():
                print 'SEARCHING...'
                search_counter += 1

                if search_counter >= 3:
                    print 'To long searching. Try reinitialise port...'
                    self.port.close()
                    time.sleep(5)
                    self._init_port(dev_path, time_out, baud_rate)
                    return

                time.sleep(1)

        except Exception as ex:
            raise OBDPortInitialiseException('Error of initialise OBD port for device "%s" (%s)' % (dev_path, ex))


    def _is_searching(self):
        self._send_command("0100")
        result = self._get_result()
        return result == 'SEARCHING...'

    def _send_command(self, command):
        self.port.flushOutput()
        self.port.flushInput()
        for c in command:
            self.port.write(c)
        self.port.write("\r\n")

    def _get_result(self, have_echo=False):
        time.sleep(0.1)
        result = ""
        c = ""
        while c != ">":
            result += c
            c = self.port.read(1)
        result_parts = result.split('\r')
        result_parts = filter(bool, result_parts)
        parts_count = len(result_parts)
        if have_echo and parts_count > 1:
            return result_parts[1]
        else:
            return result_parts[0]

    def _interpret_result(self, code):
        # Code will be the string returned from the device.
        # It should look something like this:
        # '41 11 0 0\r\r'

        # 7 seems to be the length of the shortest valid response
        if len(code) < 7:
            raise Exception("Seems like too long code: %s" % code)

        # get the first thing returned, echo should be off
        code = str(code).split("\r")[0]

        #remove whitespace
        code = code.replace(" ", "")

        if code.startswith('NODATA'):
            return 'NODATA'

        # first 4 characters are code from ELM
        code = code[4:]

        return code

