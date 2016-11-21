from pprint import pprint
from datetime import datetime


class SimpleDatastore:
    def __init__(self):
        pass

    @staticmethod
    def validate_new_client(time_stamp, age, gender, _rest):
        if isinstance(time_stamp, datetime) and isinstance(
                age, int) and age > 0 and isinstance(gender, str):
            return True
        return False

    def new_client(self, time_stamp, age, gender, rest=None):
        if self.validate_new_client(time_stamp, age, gender, rest):
            return 1
        else:
            return None

    def client_exists(self, client_id):
        return True

    def join_session(self, client_id, session_id):
        return True

    def log(self, time, data):
        pprint(time)
        pprint(data)
        return True
