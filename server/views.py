from flask import request, jsonify
from server import app, datastore, sessionstore
from pprint import pprint
from datetime import datetime


def parse_client_json(required_keys=None):
    json = request.get_json()

    print(json)
    if 'data' in json and 'time' in json:
        data = json['data']
        time = json['time']
        if isinstance(time, int) and isinstance(data, dict):
            if required_keys is not None:
                for key, required_type in required_keys:
                    if key not in data or not isinstance(data[key],
                                                         required_type):
                        break
                else:
                    return data, datetime.fromtimestamp(time)
            else:
                return data, datetime.fromtimestamp(time)
    return None, None


@app.route('/')
def index():
    return 'Hello World'


@app.route('/new_client', methods=['POST'])
def new_client():
    data, time = parse_client_json({('age', int), ('gender', str)})
    if data is not None and time is not None:
        client_id = datastore.new_client(time, data['age'], data['gender'],
                                         {k: v
                                          for (k, v) in data.items()
                                          if k != 'age' and k != 'gender'})
        if client_id is not None:
            return jsonify(success=True, client_id=client_id)
    return jsonify(success=False), 400


@app.route('/join_session', methods=['POST'])
def join_session():
    data, time = parse_client_json({('client_id', int), ('session_id', int)})
    print(sessionstore)
    if data is not None and time is not None and data[
            'session_id'] in sessionstore and datastore.client_exists(data[
                'client_id']):
        session = sessionstore[data['session_id']]
        if datastore.join_session(data['client_id'],
                                  data['session_id']) is not None:
            return jsonify(success=True,
                           channels=session.channels,
                           session_name=session.name)
    return jsonify(success=False), 400


@app.route('/log_data', methods=['POST'])
def log_data():
    data, time = parse_client_json()
    success = False if (data is None or time is None) else datastore.log(time,
                                                                         data)
    return jsonify(success=success), (200 if success else 400)
