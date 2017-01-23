from datetime import datetime

import json
import time
import http.client
import socket


class HttpSocket(http.client.HTTPConnection):

    def __init__(self, path, *args, **kwargs):
        super(HttpSocket, self).__init__(path, *args, **kwargs)
        self.path = path
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.path)


def parse_client_json(request, required_keys=None):
    try:
        json_data = json.loads(request.decode("utf-8"))

        print(json_data)
        if 'data' in json_data and 'time' in json_data:
            data = json_data['data']
            time = json_data['time']
            if isinstance(time, int) and isinstance(data, dict):
                if required_keys is not None:
                    for key, required_type in required_keys:
                        if key not in data or not isinstance(data[key],
                                                             required_type):
                            return None, None
                return data, datetime.fromtimestamp(time)
    except json.JSONDecodeError:
        pass
    return None, None

def parse_json(request):
    try:
        json_data = json.loads(request.decode("utf-8"))
        return json_data
    except json.JSONDecodeError:
        pass

    return None


def datetime_to_epoch(value):
    return int(time.mktime(value.timetuple()) * 1000)
