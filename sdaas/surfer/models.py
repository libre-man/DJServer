import os
import docker
import json
import shutil

from .utils import HttpSocket

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Session(models.Model):
    """A session is the model that contains a single silent disco.

    Each session consists of one or more channels which play music.
    """

    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    join_code = models.CharField(max_length=16)

    def __str__(self):
        return self.name

    def is_starting(self):
        return len(Channel.objects.filter(session=self, state=Channel.STARTING)) >= 1

    def has_started(self):
        return len(Channel.objects.filter(session=self, state=Channel.STARTED)) == len(Channel.objects.filter(session=self))

    def joined_clients(self):
        return len(JoinedClient.objects.filter(session=self))


class ChannelManager(models.Manager):

    def create_channel(self, session, name='Default', color='#e67e22'):
        channel = self.create(name=name, session=session, color=color)

        # Create docker container.
        client = docker.from_env()

        socket_dir = '/tmp/sdaas_controller_{}/'.format(channel.id)
        channel.socket = os.path.join(socket_dir, 'sdaas.socket')

        channel.input_dir = '/home/dj_feet/input'
        channel.output_dir = os.path.join(
            settings.OUTPUT_DIR, str(channel.id))

        os.makedirs(channel.output_dir)
        os.makedirs(get_input_dir(channel.id))

        environment = ['SDAAS_ID={}'.format(channel.id),
                       'SDAAS_INPUT_DIR={}'.format(channel.input_dir),
                       'SDAAS_OUTPUT_DIR=/home/dj_feet/output',
                       'PYTHONUNBUFFERED=False',
                       'SDAAS_REMOTE_URL={}'.format(settings.CONTROLLER_URL),
                       'SDAAS_SOCKET={}'.format(channel.socket)]

        volumes = {socket_dir: {'bind': socket_dir, 'mode': 'rw'},
                   get_input_dir(channel.id): {'bind': channel.input_dir, 'mode': 'rw'},
                   channel.output_dir: {'bind': '/home/dj_feet/output', 'mode': 'rw'}
                   }

        container = client.containers.run('controller', environment=environment,
                                          volumes=volumes, detach=True, publish_all_ports=True)

        channel.docker_id = container.id
        channel.save()
        return channel


class Channel(models.Model):
    """A channel is an entity which spawns and controls a single controller,
    which plays music automatically.
    """
    name = models.CharField(max_length=50)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    color = models.CharField(max_length=7, default='#1abc9c')

    INITIALIZING, INITIALIZED, COMMITTED, STARTING, STARTED = range(5)
    STATE_CHOICES = {
        (INITIALIZING, 'Initializing'),
        (INITIALIZED, 'Initialized'),
        (COMMITTED, 'Committed'),
        (STARTING, 'Starting'),
        (STARTED, 'Started'),
    }
    state = models.IntegerField(choices=STATE_CHOICES, default=INITIALIZING)

    # Docker fields.
    docker_id = models.CharField(max_length=100, default='')
    socket = models.CharField(max_length=100, default='')
    output_dir = models.CharField(max_length=100, default='')
    input_dir = models.CharField(max_length=100, default='')

    # Feedback
    epoch = models.BigIntegerField(default=0)

    objects = ChannelManager()

    def __str__(self):
        return '%d' % (self.id)

    def color_str(self):
        return self.color

    def start(self):
        self.state = self.STARTING
        self.save()

        request = {}

        socket = HttpSocket(self.socket)
        socket.request(method='POST', url='/start/', body=json.dumps(request),
                       headers={'Content-type': 'application/json'})
        response = socket.getresponse()
        print("starting channel")
        print(response.read().decode())

    def get_logs(self):
        client = docker.from_env()
        return client.containers.get(self.docker_id).logs()

    def get_start(self):
        # TODO: fix segment size.
        return self.epoch + 60

    def get_url(self):
        return os.path.join(settings.STREAMING_URL, str(self.id))


@receiver(pre_delete, sender=Channel)
def channel_delete(sender, instance, **kwargs):
    try:
        shutil.rmtree(instance.output_dir)
    except FileNotFoundError:
        pass

    # Delete docker
    client = docker.from_env()

    if instance.docker_id == '':
        return

    try:
        container = client.containers.get(instance.docker_id)
        container.kill()
    except (docker.errors.NotFound, docker.errors.APIError) as e:
        pass


def get_input_dir(channel_id):
    return os.path.join(settings.MEDIA_ROOT, 'channels/{}'.format(channel_id))


def file_path(instance, filename):
    return 'channels/{}/{}'.format(instance.channel.id, filename)


class FileManager(models.Manager):

    def create_file(self, channel, upload):
        instance = self.create(channel=channel, upload=upload)

        request = {'file_location': os.path.join(
            channel.input_dir, os.path.basename(instance.upload.name)), 'id': instance.id}

        socket = HttpSocket(channel.socket)
        socket.request(method='POST', url='/add_music/', body=json.dumps(request),
                       headers={'Content-type': 'application/json'})
        response = socket.getresponse()
        print(response.read().decode())

        return instance


class File(models.Model):
    """Represents an uploaded music file, used by a channel's controller to
    play music.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=file_path)

    is_processed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = FileManager()

    def filename(self):
        return os.path.basename(self.upload.name)


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    # TODO: maybe rather set the is_deleted flag and only fully delete it
    # when a music_deleted response is received.

    if instance.upload:
        if os.path.isfile(instance.upload.path):
            request = {'file_location': os.path.join(
                instance.channel.input_dir, os.path.basename(instance.upload.name))}

            try:
                socket = HttpSocket(instance.channel.socket)
                socket.request(method='POST', url='/delete_music/', body=json.dumps(request),
                               headers={'Content-type': 'application/json'})
                response = socket.getresponse()
                print(response.read().decode())
            except FileNotFoundError:
                pass

            os.remove(instance.upload.path)


class PlayedFile(models.Model):
    """To log played files by channels, PlayedFile objects are created."""
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    time_played = models.DateTimeField(auto_now_add=True)


class Client(models.Model):
    """A listener of a session. Clients are created using the Android
    application.
    """
    birth_date = models.DateField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return "{} {} {}".format(self.id, self.birth_date, self.gender)


class JoinedClient(models.Model):
    """A client becomes joined when it joins a running session."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Data(models.Model):
    """Logged data from each client is stored in Data objects."""
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    client_time = models.DateTimeField()
    server_time = models.DateTimeField(auto_now_add=True)


class ControllerPart(models.Model):
    """A part of a channel controller. This is used to set all the options
    using ControllerPartOptions.

    A part can be a communicator, controller, picker or transitioner.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    COMMUNICATOR, CONTROLLER, PICKER, TRANSITIONER = range(4)
    CATEGORY_CHOICES = {
        (COMMUNICATOR, 'Communicator'),
        (CONTROLLER, 'Controller'),
        (PICKER, 'Picker'),
        (TRANSITIONER, 'Transitioner'),
    }

    category = models.IntegerField(choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=50)
    short_doc = models.CharField(max_length=128)
    long_doc = models.TextField()

    is_set = models.BooleanField(default=False)

    def str_to_category_choice(val):
        return next(value for value, name in ControllerPart.CATEGORY_CHOICES if name.lower() == val.lower())

    def __str__(self):
        return self.name


class ControllerPartOption(models.Model):
    """A single option for a channel controller part."""
    controller_part = models.ForeignKey(
        ControllerPart, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    documentation = models.TextField()
    required = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)
    value = models.TextField(default='')
