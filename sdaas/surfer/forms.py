from django.forms import ModelForm
from django import forms

from .models import Session, Channel

class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'start', 'end']

class ChannelForm(ModelForm):
    class Meta:
        model = Channel
        fields = ['url', 'color']
