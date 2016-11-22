from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^log_data/', views.log_data, name='log_data'),
    url(r'^new_client/', views.new_client, name='new_client'),
    url(r'^join_session/', views.join_session, name='join_session'),
]
