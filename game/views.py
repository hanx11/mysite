# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.views.generic.base import View

class Game2048(View):

    def get(self, request):
        return render(request, '2048.html')

