# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    # fourteen-nobody
    url(r'^fourteen-nobody/$', views.FourteenNobodyView.as_view(), name="fourteen-nobody"),
    # 饭局酒色山河文章
    url(r'^20160920/$', views.ArticleView.as_view(), name="fengtang"),
]
