# -*- coding:utf-8 -*-

import time
import json
import hashlib
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import View
import pdb

def handleRequest(request):
    pdb.set_trace()
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type='text/plain')
        return response
    elif request.method == 'POST':
        return HttpResponse('hello')

def checkSignature(request):
    signature = request.GET.get('signature', None)
    timestamp = request.GET.get('timestamp', None)
    nonce = request.GET.get('nonce', None)
    echoStr = request.GET.get('echostr', None)
    token = 'xiaoxiao'
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = "%s%s%s" % tuple(tmplist)
    tmpstr = tmpstr.encode('utf-8')
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return HttpResponse('hello')
