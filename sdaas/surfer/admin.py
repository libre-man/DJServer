from django.contrib import admin

from .models import Session, Channel, Client, JoinedClient, ControllerPartOption, ControllerPart, File, PlayedFile

admin.site.register(Session)
admin.site.register(Channel)
admin.site.register(Client)
admin.site.register(JoinedClient)
admin.site.register(ControllerPartOption)
admin.site.register(ControllerPart)
admin.site.register(File)
admin.site.register(PlayedFile)
