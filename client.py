#!/usr/bin/env python
import json
import threading
import time

import requests
from w1thermsensor import W1ThermSensor

# SERVER_ULR = 'http://127.0.0.1:8000'
SERVER_ULR = 'http://192.168.1.101:8000'


class TempThread(threading.Thread):
    def __init__(self):
        super(TempThread, self).__init__()
        self.sensor = W1ThermSensor()
        self.is_running = True
        self.setDaemon(True)
        self.sensor_id = self.register_sensor()

    def run(self):
        while self.is_running:
            self.post_temperature(self.sensor.get_temperature())
            time.sleep(0.5)

    def stop(self):
        self.is_running = False

    def register_sensor(self):
        response = requests.get(SERVER_ULR + '/api/v1/sensors/')
        content = json.loads(response.text)

        for result in content['results']:
            if result['name'] == self.sensor.id:
                sensor_id = result['id']
                break
        else:
            payload = {'name': self.sensor.id}
            print payload
            response = requests.post(SERVER_ULR + '/api/v1/sensors/',
                                     json=payload)
            content = json.loads(response.text)
            print content
            sensor_id = content['id']
        return sensor_id

    def post_temperature(self, temperature):
        payload = {"sensor": self.sensor_id, "reading": temperature}
        response = requests.post(SERVER_ULR + '/api/v1/reading/', json=payload)
        if response.status_code == requests.codes.created:
            print '{} : temp {}'.format(response.status_code, temperature)
        else:
            print 'ERROR : {}'.format(response.status_code)




temp_thread = TempThread()
temp_thread.start()

raw_input('\n *******Press ENTER key to stop and quit program******* \n')

temp_thread.stop()
temp_thread.join()
