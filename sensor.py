import hashlib
import time
import requests
from datetime import timedelta

from homeassistant.helpers.entity import Entity

SCAN_INTERVAL = timedelta(minutes=3)

def setup_platform(hass, config, add_entities, discovery_info=None):
    token = config.get('token')
    serial_number = config.get('serial_number')
    name = config.get('name', "FoxESS")

    sensors = [
        FoxEssGenerationSensor(token, serial_number, name, "Geração do Mês", "month", "kWh"),
        FoxEssGenerationSensor(token, serial_number, name, "Geração do Dia", "today", "kWh"),
        FoxEssFeedinSensor(token, serial_number, name, "Geração Atual", "feedinPower", "kW"),
    ]
    add_entities(sensors, True)

class FoxEssGenerationSensor(Entity):
    def __init__(self, token, serial_number, base_name, sensor_name, key, unit):
        self._token = token
        self._sn = serial_number
        self._param = '/op/v0/device/generation'
        self._url = 'https://www.foxesscloud.com' + self._param + '?sn=' + self._sn
        self._key = key
        self._unit = unit
        self._name = f"{base_name} {sensor_name}"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def state(self):
        return self._state

    def update(self):
        timestamp = str(int(time.time() * 1000))
        signature_raw = f"{self._param}\\r\\n{self._token}\\r\\n{timestamp}"
        signature_md5 = hashlib.md5(signature_raw.encode('utf-8')).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'token': self._token,
            'timestamp': timestamp,
            'signature': signature_md5,
            'lang': 'en',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0'
        }

        try:
            response = requests.get(self._url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("errno") == 0:
                    result = data.get("result", {})
                    self._state = result.get(self._key)
        except Exception as e:
            print(f"Erro ao atualizar sensor FoxESS Generation: {e}")

class FoxEssFeedinSensor(Entity):
    def __init__(self, token, serial_number, base_name, sensor_name, variable, unit):
        self._token = token
        self._sn = serial_number
        self._param = '/op/v0/device/real/query'
        self._url = 'https://www.foxesscloud.com' + self._param
        self._variable = variable
        self._unit = unit
        self._name = f"{base_name} {sensor_name}"
        self._state = None

    @property
    def name(self):
        return self._name

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def state(self):
        return self._state

    def update(self):
        timestamp = str(int(time.time() * 1000))
        signature_raw = f"{self._param}\\r\\n{self._token}\\r\\n{timestamp}"
        signature_md5 = hashlib.md5(signature_raw.encode('utf-8')).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            'token': self._token,
            'timestamp': timestamp,
            'signature': signature_md5,
            'lang': 'en',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Expires': '0'
        }

        body = {
            'sn': self._sn,
            'variables': [self._variable]
        }

        try:
            response = requests.post(self._url, headers=headers, json=body, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get("errno") == 0:
                    result = data.get("result", [])
                    if result and "datas" in result[0]:
                        datas = result[0]["datas"]
                        for item in datas:
                            if item.get("variable") == self._variable:
                                self._state = item.get("value")
        except Exception as e:
            print(f"Erro ao atualizar sensor FoxESS Feed-in Power: {e}")
