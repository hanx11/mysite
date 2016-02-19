# -*- coding:utf-8 -*-

import os
import time
import json
import hashlib
import requests
import xml.etree.ElementTree as ET
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
import pdb


TOKEN = "xiaoxiao"
YOUDAO_KEY_FROM = "hanfeng"
YOUDAO_KEY = "692856525"
YOUDAO_DOC_TYPE = "xml"

def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    else:
        return None

def checkSignature(request):
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

def parse_msg(request):
    # 解析来自微信的请求，request用于传递请求信息
    recvmsg = request.body 
    root = ET.fromstring(recvmsg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg

def parseYouDaoResponse(rep):
    replyContent = ''
    # pdb.set_trace()
    result = json.loads(rep.text, encoding='utf-8')
    errorCode = result.get('errorCode')
    print(errorCode)
    # 错误码检查
    if errorCode == '20':
        replyContent = "Too long to translate\n"
        return replyContent
    elif errorCode == '30':
        replyContent = "Can not be able to translate with effect\n"
        return replyContent
    elif errorCode == '40':
        replyContent = "Can not be able to support this language\n"
        return replyContent
    elif errorCode == '50':
        replyContent = "Invalid key\n"
        return replyContent
    elif errorCode == '0':
        queryData = result.get('query')
        translation = result.get('translation', '123')[0].encode('utf-8')
        basicPhonetic = result.get('basic').get('phonetic')
        basicExplains = result.get('basic').get('explains')[0]
        # print(translation)
        replyContent = translation
        return replyContent

def getReplyXml(msg,replyContent):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[%s]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>";
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),'text',replyContent)
    return extTpl


class WeixinInterfaceView(View):
    def get(self, request):
        # 得到GET内容
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        #自己的token
        token = 'xiaoxiao'   #这里改写你在微信公众平台里输入的token
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
        msg = parse_msg(request)           #进行XML解析
        toUserName = msg['ToUserName']
        fromUserName = msg['FromUserName']
        createTime = msg['CreateTime']
        msgType = msg['MsgType']
        content = msg['Content']   #获得用户所输入的内容
        msgId = msg['MsgId']
        return render(request, 'reply_text.xml',
                      {'toUserName': fromUserName,
                       'fromUserName': toUserName,
                       'createTime': time.time(),
                       'msgType': msgType,
                       'content': content,
                       },
                       content_type = 'application/xml'
        )


class YouDaoInterfaceView(View):
    def get(self, request):
        return HttpResponse(checkSignature(request), content_type="text/plain")

    def post(self, request):
        msg = parse_msg(request)      #进行xml解析
        pdb.set_trace()
        queryStr = msg.get('Content', 'You have input nothing~').decode('ascii').encode('utf-8')
        # print(msg.get('Content').encode('utf-8'))
        query_data = {'keyfrom':'hanfeng', 'key':'692856525', 'type':'data', 'doctype':'json', 'version':'1.1', 'q':queryStr}
        response = requests.get("http://fanyi.youdao.com/openapi.do", params=query_data)
        replyContent = parseYouDaoResponse(response)
        toUserName = msg['ToUserName']
        fromUserName = msg['FromUserName']
        createTime = msg['CreateTime']
        msgType = msg['MsgType']
        msgId = msg['MsgId']
        return render(request, 'reply_text.xml',
                      {'toUserName': fromUserName,
                       'fromUserName': toUserName,
                       'createTime': time.time(),
                       'msgType': msgType,
                       'content': replyContent,
                       },
                       content_type = 'application/xml'
        )

