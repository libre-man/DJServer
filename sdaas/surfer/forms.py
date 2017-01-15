from django.forms import ModelForm, DateTimeInput
from django import forms

from .models import Session, Channel
from .widgets import ColorPicker


class SessionForm(ModelForm):

    class Meta:
        model = Session
        fields = ('name', 'start', 'end', 'join_code')
        widgets = {
            'start': DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'placeholder': '2017-01-13 14:30:59'}),
            'end': DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'placeholder': '2017-01-13 14:30:59'}),
        }
        help_texts = {
            'start': 'The start date and time of the session',
            'end': 'The end date and time of the session',
            'join_code': 'The code clients need to enter to join this session',
        }


class ChannelForm(ModelForm):

    class Meta:
        model = Channel
        fields = ['name', 'color']

        widgets = {
            'color': ColorPicker()
        }


class UploadFileForm(forms.Form):
    upload = forms.FileField()
