from django.forms.widgets import TextInput


class ColorPicker(TextInput):
    input_type = 'color'

    def value_from_datadict(self, data, files, name):
        return data.get(name)

    def render(self, name, value, attrs=None):
        if value is None:
            value = "#000000"

        return super(ColorPicker, self).render(name, value, attrs)
