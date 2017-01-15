from django.forms import ModelForm, DateTimeInput
from django import forms

from .models import Session, Channel


class SessionForm(ModelForm):

    class Meta:
        model = Session
        fields = ('name', 'start', 'end')
        widgets = {
            'start': DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'placeholder': '2017-01-13 14:30:59'}),
            'end': DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'placeholder': '2017-01-13 14:30:59'}),
        }
        help_texts = {
            'name': 'The name of the session',
            'start': 'The start date and time of the session',
            'end': 'The end date and time of the session',
        }


class ChannelForm(ModelForm):

    class Meta:
        model = Channel
        fields = ['url', 'color']


class UploadFileForm(forms.Form):
    upload = forms.FileField()
