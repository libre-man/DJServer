import time
import json

from django.test import TestCase, Client

from ..testing_utilities import populate_test_db
from surfer import models as s

class RequestTests(TestCase):

    def setUp(self):
        self.client = Client()
        populate_test_db()

    def test_new_client(self):
        data = {'time': int(time.time()), 'data': {
                'name': 'testname',
                'birth_date': int(time.time())
            }}

        response = self.client.post('/new_client/', json.dumps(data),
                content_type='application/json')

        self.assertEqual(len(s.Client.objects.filter(name='testname')), 1)
        c = s.Client.objects.filter(name='testname').last()

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])
        self.assertEqual(content['client_id'], c.id)

    def test_join_session(self):
        client = s.Client.objects.filter(name='unjoinedclient')[0]
        session = s.Session.objects.filter(name='test_session')[0]

        data = {'time': int(time.time()), 'data': {
                'client_id': client.id,
                'session_id': session.id
            }}

        response = self.client.post('/join_session/', json.dumps(data),
                content_type='application/json')

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])
        self.assertEquals(content['session_name'], 'test_session')
        self.assertEquals(len(content['channels']), 2)

    def test_log_data_valid(self):
        client = s.Client.objects.filter(name='client')[0]
        jclient = s.JoinedClient.objects.filter(client=client)[0]
        session = jclient.session

        data = {'time': int(time.time()), 'data': {
                    'client_id': client.id,
                    'session_id': session.id
                }}

        response = self.client.post('/log_data/', json.dumps(data),
                content_type='application/json')

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertTrue(content['success'])

    def test_log_data_invalid(self):
        response = self.client.post('/log_data/', '{"time":293084',
                content_type='application/json')
 
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertFalse(content['success'])

    def test_log_data_empty(self):
        response = self.client.post('/log_data/', '',
                content_type='application/json')

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode('utf-8'))
        self.assertFalse(content['success'])

