# -*- coding:utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'blog'

urlpatterns = [
    # fourteen-nobody
    url(r'^fourteen-nobody/$', views.FourteenNobodyView.as_view(), name="fourteen-nobody"),
    # 饭局酒色山河文章
    url(r'^cate-wine-beautiful-essay/$', views.ArticleView.as_view(), name="cate-wine-beautiful-essay"),
    # 小猪大道
    url(r'^little-pig-big-road/$', views.LittlePigView.as_view(), name="little-pig-big-road"),
    # 日常生活的革命
    url(r'daily-life/$', DailyLifeView.as_view(), name="daily-life"),
]
