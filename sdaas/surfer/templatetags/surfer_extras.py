from django import template

register = template.Library()


@register.filter(name="addstr")
def addstr(arg1, arg2):
    return str(arg1) + str(arg2)


@register.filter(name="addcss")
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
