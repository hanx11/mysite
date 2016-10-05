# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

class FourteenNobodyView(View):

    def get(self, request):
        return render(request, 'fourteen-nobody.html')


class ArticleView(View):

    def get(self, request):
        return render(request, '20160920.html')


class LittlePigView(View):

    def get(self, request):
        return render(request, 'little-pig-big-road.html')

class DailyLifeView(View):

    def get(self, request):
        return render(request, 'daily-life.html')

