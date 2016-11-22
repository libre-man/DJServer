from django.db import models
from django.contrib.auth.models import User


class Session(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)


class Channel(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    url = models.URLField()
    color = models.IntegerField()


class Client(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)


class JoinedClient(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Data(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    client_time = models.DateField()
    server_time = models.DateField(auto_now_add=True)
