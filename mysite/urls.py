"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from mysite import views
from mysite.views import handleRequest
# from mysite.views import WeixinInterfaceView, YouDaoInterfaceView, handleRequest
# from mysite.views import weiXinInterfaceView
from django.views.decorators.csrf import csrf_exempt    #remove csrf

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', csrf_exempt(handleRequest), name='handleRequest'),
    # url(r'^$', csrf_exempt(views.weiXinInterfaceView), name='handleWeiXinRequest'),
    # url(r'^$', csrf_exempt(views.WeixinInterfaceView.as_view()), name='handleWeiXinRequest'),

    # url(r'^$', csrf_exempt(views.YouDaoInterfaceView.as_view()), name='handleWeiXinRequest'),
]
