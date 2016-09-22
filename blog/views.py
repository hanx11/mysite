# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

class FourteenNobodyView(View):

    def get(self, request):
        return render(request, 'fourteen-nobody.html')


class ArticleView(View):

    def get(self, request):
        return render(request, '20160920.html')


class LittePigView(View):

    def get(self, request):
        return render(request, 'litte-pig-big-road.html')

