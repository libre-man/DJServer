import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from . import utils
from .models import Client, Session, JoinedClient, Channel


def index(request):
    return HttpResponse('Hello, World!')


@csrf_exempt
def new_client(request):
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(request.body, {('name', str), ('birth_date', int)})

        if data is not None and time is not None:
            client = Client(name=data['name'], birth_date=timezone.now())
            client.save()

            response_data['success'] = True
            response_data['client_id'] = client.id

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


@csrf_exempt
def join_session(request):
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(request.body,
                                             {('client_id', int),
                                              ('session_id', int)})

        if data is not None and time is not None:
            try:
                c = Client.objects.get(id=data['client_id'])
                s = Session.objects.get(id=data['session_id'])

                if not JoinedClient.objects.filter(client=c, session=s):
                    joined_client = JoinedClient(client=c, session=s)
                    joined_client.save()

                response_data['success'] = True
                response_data['session_name'] = s.name
                channels = Channel.objects.filter(session=s)

                response_data['channels'] = []
                for c in channels:
                    response_data['channels'].append({'channel_id': c.id,
                                                      'color': c.color,
                                                      'url': c.url})

                response_data['session_start'] = utils.datetime_to_epoch(s.start)
            except ObjectDoesNotExist:
                response_data['error'] = 'Client or session does not exist'

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


@csrf_exempt
def log_data(request):
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(request.body)

        if data is not None and time is not None:
            response_data['success'] = True

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')
