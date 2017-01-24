from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # Session:
    url(r'^session/add/$', views.add_session, name='add_session'),
    url(r'^session/(?P<session_id>[0-9]+)/$',
        views.session_detail, name='session_detail'),
    url(r'^session/(?P<session_id>[0-9]+)/edit/$',
        views.session_edit, name='session_edit'),
    url(r'^session/(?P<session_id>[0-9]+)/delete/$',
        views.session_delete, name='session_delete'),
    url(r'^session/(?P<session_id>[0-9]+)/settings/$',
        views.session_settings, name='session_settings'),
    url(r'^session/(?P<session_id>[0-9]+)/start/$',
        views.session_start, name='session_start'),

    # Channel:
    url(r'^session/(?P<session_id>[0-9]+)/channel/add/$',
        views.add_channel, name='add_channel'),
    url(r'^channel/(?P<channel_id>[0-9]+)/$',
        views.channel_detail, name='channel_detail'),
    url(r'^channel/(?P<channel_id>[0-9]+)/edit/$',
        views.channel_edit, name='channel_edit'),
    url(r'^channel/(?P<channel_id>[0-9]+)/delete/$',
        views.channel_delete, name='channel_delete'),
    url(r'^channel/(?P<channel_id>[0-9]+)/upload/$',
        views.channel_upload, name='channel_upload'),
    url(r'^channel/(?P<channel_id>[0-9]+)/settings/$',
        views.channel_settings, name='channel_settings'),
    url(r'^channel/(?P<channel_id>[0-9]+)/settings/(?P<category_id>[0-9]+)/$',
        views.channel_part_options, name='channel_part_options'),

    # Files:
    url(r'^file/(?P<file_id>[0-9]+)/delete/$',
        views.file_delete, name='file_delete'),

    # API urls:
    url(r'^log_data/', views.log_data, name='log_data'),
    url(r'^new_client/', views.new_client, name='new_client'),
    url(r'^join_session/', views.join_session, name='join_session'),

    # Controller->Server API urls:
    url(r'^im_alive/', views.im_alive, name='im_alive'),
    url(r'^iteration/', views.iteration, name='iteration'),
    url(r'^music_processed/', views.music_processed, name='music_processed'),
    url(r'^music_deleted/', views.music_deleted, name='music_deleted'),
    url(r'^get_feedback/', views.get_feedback, name='get_feedback'),
    url(r'^controller_started/', views.controller_started,
        name='controller_started'),
]
