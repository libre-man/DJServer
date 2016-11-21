from django.db import models
from django.contrib.auth.models import User

class Session:
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start = models.DateField()
    end = models.DateField()
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)


class Channel:
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Client:
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    created = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)


class Data:
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    client_time = models.DateField()
    server_time = models.DateField(auto_now_add=True)
