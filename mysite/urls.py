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

from . import views
from django.views.decorators.csrf import csrf_exempt    #remove csrf

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    # Home Page
    url(r'^$', views.HomePageView.as_view(), name='home-page'),
    # about
    url(r'^about/$', views.AboutView.as_view(), name='about'),
    # Blog urls
    url(r'^blog/', include('blog.urls')),
    # Game urls
    url(r'^game/', include('game.urls')),

    # url(r'^$', csrf_exempt(WeixinInterfaceView.as_view()), name='handleWeiXinRequest'),
    # url(r'^$', csrf_exempt(YouDaoInterfaceView.as_view()), name='handleWeiXinRequest'),
]
