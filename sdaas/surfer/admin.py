from django.contrib import admin

from .models import Session, Channel, Client, JoinedClient

admin.site.register(Session)
admin.site.register(Channel)
admin.site.register(Client)
admin.site.register(JoinedClient)
