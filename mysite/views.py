# -*- coding:utf-8 -*-

import os
import time
import hashlib
import json
from lxml import etree
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse

def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    elif request.method == 'POST':
    	return HttpResponse("hello world")

def checkSignature(request):
	TOKEN = "hanfeng"
	signature = request.GET.get("signature", None)  
	timestamp = request.GET.get("timestamp", None)  
	nonce = request.GET.get("nonce", None)  
	echoStr = request.GET.get("echostr", None)  

	token = TOKEN  
	tmpList = [token, timestamp, nonce]  
	tmpList.sort()  
	tmpstr = "%s%s%s" % tuple(tmpList)
	tmpstr = tmpstr.encode('utf-8')  
	tmpstr = hashlib.sha1(tmpstr).hexdigest()  
	if tmpstr == signature:
		return echoStr  
	else:
		return None 


class WeixinInterfaceView(View):
    def get(self, request):
        #得到GET内容
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #自己的token
        token = 'yourtoken' #这里改写你在微信公众平台里输入的token
        #字典序排序
        tmpList = [token, timestamp, nonce]
        tmpList.sort()
        tmpstr = '%s%s%s' % tuple(tmpList)
        tmpstr = tmpstr.encode('utf-8')
        #sha1加密算法
        tmpstr = hashlib.sha1(tmpstr).hexdigest()
        
        #如果是来自微信的请求，则回复echostr
        if tmpstr == signature:
            return render(request, 'get.html', {'str': echostr},
                          content_type='text/plain')
    def post(self, request):
        str_xml = request.body.decode('utf-8')    #use body to get raw data
        xml = etree.fromstring(str_xml)    #进行XML解析
        
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text
        content = xml.find('Content').text   #获得用户所输入的内容
        msgId = xml.find('MsgId').text
        return render(request, 'reply_text.xml',
                      {'toUserName': fromUserName,
                       'fromUserName': toUserName,
                       'createTime': time.time(),
                       'msgType': msgType,
                       'content': content,
                       },
                       content_type = 'application/xml'
        )

