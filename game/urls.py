# -*- coding:utf-8 -*-

from django.conf.urls import include, url
from . import views

app_name = 'game'

urlpatterns = [
    url(r'^2048/$', views.Game2048.as_view(), name="game-2048"),
]
