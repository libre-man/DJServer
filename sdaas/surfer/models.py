from django.db import models
from django.contrib.auth.models import User


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
