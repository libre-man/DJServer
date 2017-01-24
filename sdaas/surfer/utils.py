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


class AutoCast:
    """Source: https://github.com/cgreer/cgAutoCast"""

    @staticmethod
    def boolify(s):

        if s == 'True' or s == 'true':
            return True
        if s == 'False' or s == 'false':
            return False
        raise ValueError('Not Boolean Value!')

    @staticmethod
    def noneify(s):
        ''' for None type'''
        if s.lower() == 'none':
            return None
        raise ValueError('Not None Value!')

    def listify(self, s):
        '''will convert a string representation of a list
        into list of homogenous basic types.  type of elements in
        list is determined via first element and successive
        elements are casted to that type'''

        # this cover everything?
        if "," not in s:
            raise ValueError('Not a List')

        # derive the type of the variable
        loStrings = s.split(',')
        elementCaster = None
        for caster in (self.boolify, int, float, self.noneify, str):
            try:
                caster(loStrings[0])
                elementCaster = caster
                break
            except ValueError:
                pass

        # cast all elements
        try:
            castedList = [elementCaster(x) for x in loStrings]
        except ValueError:
            raise TypeError("Autocasted list must be all same type")

        return castedList

    def __call__(self, var):
        '''guesses the str representation of the variable's type'''

        # dont need to guess type if it is already un-str typed (not coming
        # from CLI)
        if type(var) != type('aString'):
            return var

        # guess string representation, will default to string if others dont
        # pass
        for caster in (self.boolify, int, float, self.noneify, self.listify, str):
            try:
                return caster(var)
            except ValueError:
                pass


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
