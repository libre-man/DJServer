from django.forms import ModelForm, DateTimeInput
from django import forms

from .models import Session, Channel, ControllerPart, ControllerPartOption
from .widgets import ColorPicker


class SessionForm(ModelForm):

    class Meta:
        model = Session
        fields = ('name', 'start', 'end', 'join_code')
        widgets = {
            'start': DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                   attrs={'placeholder': '2017-01-13 14:30:59'}),
            'end': DateTimeInput(format='%Y-%m-%d %H:%M:%S',
                                 attrs={'placeholder': '2017-01-13 14:30:59'}),
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


class PartSelectForm(forms.Form):

    def __init__(self, channel, *args, **kwargs):
        super(PartSelectForm, self).__init__(*args, **kwargs)

        for cat_id, cat_name in ControllerPart.CATEGORY_CHOICES:
            parts = ControllerPart.objects.filter(
                category=cat_id, channel=channel)

            self.fields[cat_name] = forms.ModelChoiceField(
                queryset=parts, empty_label="Not set")

            self.fields[cat_name].help_text = ''
            for p in parts:
                self.fields[
                    cat_name].help_text += '<div class="part-help">{}<br/>{}</div>'.format(p.name, p.long_doc)


class PartOptionForm(forms.Form):

    def __init__(self, controller_part, *args, **kwargs):
        super(PartOptionForm, self).__init__(*args, **kwargs)

        options = ControllerPartOption.objects.filter(
            controller_part=controller_part, fixed=False)

        for option in options:
            self.fields[option.name] = forms.CharField(
                required=option.required)
            self.fields[option.name].help_text = option.documentation
