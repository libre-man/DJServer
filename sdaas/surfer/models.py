import os

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
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name


class ChannelManager(models.Manager):

    def create_channel(self, session, name="Default", color=0):
        channel = self.create(name=name, session=session, color=color)

        # TODO: Create docker container.

        return channel


class Channel(models.Model):
    """A channel is an entity which spawns and controls a single controller,
    which plays music automatically.
    """
    name = models.CharField(max_length=50)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    url = models.URLField(null=True)
    color = models.IntegerField()
    is_initialized = models.BooleanField(default=False)

    objects = ChannelManager()

    def __str__(self):
        return '%d: %s' % (self.id, self.url)

    def color_str(self):
        return '#%0.6X' % self.color


@receiver(pre_delete, sender=Channel)
def channel_delete(sender, instance, **kwargs):
    # TODO: Kill docker container.
    pass


def file_path(instance, filename):
    return 'channels/{}/{}'.format(instance.channel.id, filename)


class FileManager(models.Manager):

    def create_file(self, channel, upload):
        instance = self.create(channel=channel, upload=upload)

        # TODO: Send request to channel docker container: /add_music

        return instance


class File(models.Model):
    """Represents an uploaded music file, used by a channel's controller to
    play music.
    """
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=file_path)
    is_processed = models.BooleanField(default=False)

    objects = FileManager()

    def filename(self):
        return os.path.basename(self.upload.name)


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    # TODO: send request to docker container: /delete_music

    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)


class PlayedFile(models.Model):
    """To log played files by channels, PlayedFile objects are created."""
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
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


class ControllerPartOption(models.Model):
    """A single option for a channel controller part."""
    controller_part = models.ForeignKey(
        ControllerPart, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    documentation = models.TextField()
    required = models.BooleanField(default=False)
    fixed = models.BooleanField(default=False)
