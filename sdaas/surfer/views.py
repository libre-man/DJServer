import json
import datetime

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from . import utils
from .models import Client, Session, JoinedClient, Channel, File, ControllerPart, ControllerPartOption
from .forms import SessionForm, UploadFileForm, ChannelForm


@login_required
def index(request):
    sessions = Session.objects.filter(host=request.user)

    return render(request, 'index.html', {'sessions': sessions})


# Session views
# -----------------------------------------------------------------------------

@login_required
def session_detail(request, session_id):
    session = Session.objects.get(id=session_id, host=request.user)

    if session is not None:
        channels = Channel.objects.filter(session=session)

    return render(request, 'session_detail.html', {'session': session, 'channels': channels})


@login_required
def session_settings(request, session_id):
    return HttpResponse()


@login_required
@permission_required('surfer.add_session')
def add_session(request):
    if request.method == 'POST':
        form = SessionForm(request.POST)

        if form.is_valid():
            new_session = form.save(commit=False)
            new_session.host = request.user
            new_session.save()

            # Create default channel
            new_channel = Channel.objects.create_channel(session=new_session)

            return HttpResponseRedirect('/session/{}/'.format(new_session.id))

    else:
        form = SessionForm()

    return render(request, 'add_session.html', {'form': form})


@login_required
@permission_required('surfer.change_session')
def session_edit(request, session_id):
    instance = Session.objects.get(pk=session_id)

    if request.method == 'POST':
        form = SessionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/session/{}/'.format(session_id))

    else:
        form = SessionForm(instance=instance)

    return render(request, 'edit_session.html', {'form': form, 'session_id': session_id})


@login_required
@permission_required('surfer.delete_session')
def session_delete(request, session_id):
    instance = Session.objects.get(pk=session_id)

    if instance is not None:
        instance.delete()

    return HttpResponseRedirect('/')


# Channel views
# -----------------------------------------------------------------------------

@login_required
def channel_detail(request, channel_id):
    channel = Channel.objects.get(id=channel_id)

    if channel is not None:
        files = File.objects.filter(channel=channel)
        form = UploadFileForm()

    return render(request, 'channel_detail.html', {'channel': channel, 'files': files, 'form': form})


@login_required
@permission_required('surfer.add_channel')
def add_channel(request, session_id):
    session = Session.objects.get(pk=session_id)

    if request.method == 'POST':
        form = ChannelForm(request.POST)

        if form.is_valid():
            new_channel = form.save(commit=False)
            Channel.objects.create_channel(
                name=new_channel.name, color=new_channel.color, session=session)
            return HttpResponseRedirect('/session/{}/'.format(session_id))

    else:
        form = ChannelForm()

    return render(request, 'add_channel.html', {'form': form, 'session': session})


@login_required
@permission_required('surfer.change_channel')
def channel_edit(request, channel_id):
    instance = Channel.objects.get(pk=channel_id)

    if request.method == 'POST':
        form = ChannelForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/channel/{}/'.format(instance.id))

    else:
        form = ChannelForm(instance=instance)

    return render(request, 'edit_channel.html', {'form': form, 'channel_id': channel_id})


@login_required
@permission_required('surfer.delete_channel')
def channel_delete(request, channel_id):
    instance = Channel.objects.get(pk=channel_id)

    if instance is not None:
        session_id = instance.session.id
        instance.delete()

        return HttpResponseRedirect('/session/{}/'.format(session_id))

    return HttpResponseRedirect('/')


# Music file upload
# -----------------------------------------------------------------------------

@login_required
def channel_upload(request, channel_id):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            File.objects.create_file(upload=request.FILES['upload'],
                                     channel=Channel.objects.get(id=channel_id))

    return HttpResponseRedirect('/channel/{}/'.format(channel_id))


@login_required
def file_delete(request, file_id):
    f = File.objects.get(pk=file_id)
    f.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Client->Server protocol methods
# -----------------------------------------------------------------------------

@csrf_exempt
def new_client(request):
    """Lets a new Android application create a client on the server."""
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(
            request.body, {('birth_year', int), ('birth_month', int), ('birth_day', int), ('gender', str)})

        if data is not None and time is not None:
            client = Client(gender=data['gender'],
                            birth_date=datetime.date(data['birth_year'],
                                                     data['birth_month'],
                                                     data['birth_day']))
            client.save()

            response_data['success'] = True
            response_data['client_id'] = client.id

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


@csrf_exempt
def join_session(request):
    """Lets a client Android application join a session.

    Returns a JSON response containing all the channels in the session and
    the session name.
    """
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
    """Saves data into the database.

    This method is called by joined Android clients every n (configurable by
    the application) seconds.
    """
    response_data = {}
    response_data['success'] = False

    if request.method == 'POST':
        data, time = utils.parse_client_json(request.body)

        if data is not None and time is not None:
            response_data['success'] = True

    return HttpResponse(json.dumps(response_data),
                        content_type='application/json')


# Controller->Server protocol methods
# -----------------------------------------------------------------------------

@csrf_exempt
def im_alive(request):
    """Callback for when a channel controller is fully initialized and the web
    server is running.

    Expected JSON: { 'id': int,
                     'options': {
                          subject: {
                              part {
                                  option_name: option in part options
                              }
                              in parts
                          }
                          in subjects
                     }
                    }
    option is of the type:
        { 'name': string, 'doc': string, 'required': bool, 'fixed': bool }
    """
    if request.method == 'POST':
        data = utils.parse_json(request.body)

        if 'id' in data and isinstance(data['id'], int):
            instance = Channel.objects.get(pk=data['id'])

            if instance is not None:
                instance.is_initialized = True
                instance.save()

                # TODO: refactor.
                # TODO: handle bad cases.
                for subject, parts in data['options'].items():
                    category = ControllerPart.str_to_category_choice(subject)

                    for name, part in parts.items():
                        controller_part = ControllerPart(
                            channel=instance, name=name, category=category)
                        controller_part.save()

                        for part_option_name, part_option in part.items():
                            opt = ControllerPartOption(
                                controller_part=controller_part,
                                name=part_option_name,
                                documentation=part_option['doc'],
                                required=part_option['required'],
                                fixed=part_option['fixed'])
                            opt.save()
    return HttpResponse()


@csrf_exempt
def iteration(request):
    """Callback for a channel controller iteration.

    Expected JSON: { 'id': int, 'file_mixed': string }
    """
    return HttpResponse()


@csrf_exempt
def music_processed(request):
    """Callback for when a music file is processed by a channel controller.

    Expected JSON: { 'id': int }
    """
    if request.method == 'POST':
        data = utils.parse_json(request.body)

        if isinstance(data["id"], int):
            instance = File.objects.get(pk=data["id"])

            if instance is not None:
                instance.is_processed = True
                instance.save()

    return HttpResponse()


@csrf_exempt
def music_deleted(request):
    """Callback for when the channel controller is finished deleting a music
    file.
    """
    return HttpResponse()


@csrf_exempt
def get_feedback(request):
    """API call from a channel controller to get feedback in a certain
    timeframe.
    """
    return HttpResponse()


@csrf_exempt
def controller_started(request):
    """Callback for when a channel controller has started succesfully.

    Expected JSON: { 'id': int, 'epoch': int }
    """
    return HttpResponse()
