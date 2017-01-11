from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Session:
    url(r'^session/add/$', views.add_session, name='add_session'),
    url(r'^session/(?P<session_id>[0-9]+)/$', views.session_detail, name='session_detail'),
    url(r'^session/(?P<session_id>[0-9]+)/edit/$', views.session_edit, name='session_edit'),
    url(r'^session/(?P<session_id>[0-9]+)/delete/$', views.session_delete, name='session_delete'),

    # Channel:
    url(r'^session/(?P<session_id>[0-9]+)/channel/add/$', views.add_channel, name='add_channel'),
    url(r'^channel/(?P<channel_id>[0-9]+)/$', views.channel_detail, name='channel_detail'),
    url(r'^channel/(?P<channel_id>[0-9]+)/delete/$', views.channel_delete, name='channel_delete'),

    # API urls:
    url(r'^log_data/', views.log_data, name='log_data'),
    url(r'^new_client/', views.new_client, name='new_client'),
    url(r'^join_session/', views.join_session, name='join_session'),
]
