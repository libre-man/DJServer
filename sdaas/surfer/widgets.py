from django.forms.widgets import TextInput


class ColorPicker(TextInput):
    input_type = 'color'

    def value_from_datadict(self, data, files, name):
        return int(data.get(name)[1:], 16)

    def render(self, name, value, attrs=None):
        return super(ColorPicker, self).render(name, '#%0.6X' % value, attrs)
