import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from . import utils
from .models import Client, Session, JoinedClient, Channel, File
from .forms import SessionForm, UploadFileForm


@login_required
def index(request):
    sessions = Session.objects.filter(host=request.user)

    return render(request, 'index.html', {'sessions': sessions})


@login_required
@permission_required('surfer.add_session')
def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            new_session = form.save(commit=False)
            new_session.host = request.user
            new_session.save()
            return HttpResponseRedirect('/session/{}/'.format(new_session.id))

    else:
        form = SessionForm()

    return render(request, 'add_session.html', {'form': form})


@login_required
def session_detail(request, session_id):
    session = Session.objects.get(id=session_id, host=request.user)

    if session is not None:
        channels = Channel.objects.filter(session=session)

    return render(request, 'session_detail.html', {'session': session, 'channels': channels})


@login_required
@permission_required('surfer.change_session')
def session_edit(request, session_id):
    return HttpResponse()


@login_required
@permission_required('surfer.delete_session')
def session_delete(request, session_id):
    return HttpResponse()


@login_required
@permission_required('surfer.add_channel')
def add_channel(request, session_id):
    return HttpResponse()


@login_required
@permission_required('surfer.delete_channel')
def channel_delete(request, channel_id):
    return HttpResponse()


@login_required
def channel_detail(request, channel_id):
    channel = Channel.objects.get(id=channel_id)

    if channel is not None:
        files = File.objects.filter(channel=channel)
        form = UploadFileForm()

    return render(request, 'channel_detail.html', {'channel': channel, 'files': files, 'form': form})


@login_required
def channel_upload(request, channel_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            instance = File(upload=request.FILES[
                            'upload'], channel=Channel.objects.get(id=channel_id))
            instance.save()

    return HttpResponseRedirect('/channel/{}/'.format(channel_id))


@login_required
def file_delete(request, file_id):
    f = File.objects.get(pk=file_id)
    f.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def new_client(request):
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(
            request.body, {('name', str), ('birth_date', int)})

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

                response_data[
                    'session_start'] = utils.datetime_to_epoch(s.start)
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
