import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Session(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    join_code = models.CharField(max_length=16)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name


class Channel(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    url = models.URLField()
    color = models.IntegerField()

    def __str__(self):
        return '%d: %s' % (self.id, self.url)

    def color_str(self):
        return '#%0.6X' % self.color


def file_path(instance, filename):
    return 'channels/{}/{}'.format(instance.channel.id, filename)


class File(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    upload = models.FileField(upload_to=file_path)

    def filename(self):
        return os.path.basename(self.upload.name)


@receiver(pre_delete, sender=File)
def file_delete(sender, instance, **kwargs):
    if instance.upload:
        if os.path.isfile(instance.upload.path):
            os.remove(instance.upload.path)


class Client(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()

    def __str__(self):
        return self.name


class JoinedClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Data(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    client_time = models.DateTimeField()
    server_time = models.DateTimeField(auto_now_add=True)
