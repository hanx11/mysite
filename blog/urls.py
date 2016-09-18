# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    # fourteen-nobody
    url(r'^fourteen-nobody/$', views.FourteenNobodyView.as_view(), name="fourteen-nobody"),
]
