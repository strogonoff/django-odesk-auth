#coding: utf-8

from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns('',
    url(r'^authenticate/', views.oauth_login,
        name='odesk_oauth_login'),
    url(r'^callback/', views.oauth_login_callback,
        name='odesk_oauth_login_callback'),
    url(r'^check-login/', views.oauth_check_login,
        name='odesk_oauth_check_login'),
)
