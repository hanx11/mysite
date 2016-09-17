# -*- coding:utf-8 -*-

import os
import sys
import time
import json
import hashlib
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
import pdb


TOKEN = "xiaoxiao"
YOUDAO_KEY_FROM = "hanfeng"
YOUDAO_KEY = "692856525"
YOUDAO_DOC_TYPE = "xml"


class HomePageView(View):
    
    def get(self, request):
        return render(request, 'fourteen-nobody.html')

class IndexPageView(View):

    def get(self, request):
        return render(request, 'index.html')

def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    else:
        return None

def checkSignature(request):
    # 检查微信服务器发来的请求
    signature = request.GET.get("signature", "")  
    timestamp = request.GET.get("timestamp", "")
    nonce = request.GET.get("nonce", "")
    echoStr = request.GET.get("echostr", "")  
    token = TOKEN  
    tmpList = [token, timestamp, nonce]  
    tmpList.sort()  
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = tmpstr.encode('utf-8')  
    tmpstr = hashlib.sha1(tmpstr).hexdigest()  
    if tmpstr == signature:
        return "hello"
    else:
        return None 

def parse_msg(request):
    # 解析来自微信的请求，request用于传递请求信息
    msg = {}
    content = request.body.decode('utf-8', 'ignore')
    print(content.encode('utf-8'))
    soup = BeautifulSoup(content, 'html.parser')
    msg['ToUserName'] = soup.tousername.text
    msg['FromUserName'] = soup.fromusername.text
    msg['Content'] = soup.content.text
    msg['MsgId'] = soup.msgid.text
    msg['MsgType'] = soup.msgtype.text
    return msg

def parseYouDaoResponse(response):
    # 解析有道翻译返回的内容
    replyContent = ''
    content = response.content.decode('utf-8', errors='ignore')
    result = json.loads(content)
    errorCode = result.get('errorCode')
    # queryData = result.get('query')
    print(errorCode)
    # 错误码检查
    if errorCode == 20:
        replyContent = "Too long to translate\n"
        return replyContent
    elif errorCode == 30:
        replyContent = "Can not be able to translate with effect\n"
        return replyContent
    elif errorCode == 40:
        replyContent = "Can not be able to support this language\n"
        return replyContent
    elif errorCode == 50:
        replyContent = "Invalid key\n"
        return replyContent
    elif errorCode == 0:
        explain = ''
        queryData = result.get('query')
        print(queryData.encode('utf-8'))
        try:
            translation = result.get('translation')[0]
            basic = result.get('basic', 'None')
            explains = basic.get('explains', 'None')
            print(explains)
        except Exception as e:
            if basic is 'None':
                replyContent = "%s\n--有道翻译--\n翻译:\n%s\n" % (queryData, translation)
        else:
            if explains is not 'None':
                for exp in explains:
                    explain = explain + '\n\t' + exp
                replyContent = "%s\n--有道翻译--\n翻译:%s\n解释:%s\n" % (queryData, translation, explain)  
        finally:
            return replyContent


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
        queryStr = msg['Content']
        query_data = {'keyfrom':'hanfeng', 'key':'692856525', 'type':'data', 'doctype':'json', 'version':'1.1', 'q':queryStr}
        response = requests.get("http://fanyi.youdao.com/openapi.do", params=query_data)
        print(response.content)
        replyContent = parseYouDaoResponse(response)
        toUserName = msg['ToUserName']
        fromUserName = msg['FromUserName']
        createTime = time.time()
        msgType = msg['MsgType']
        msgId = msg['MsgId']
        return render(request, 'reply_text.xml',
                      {'toUserName': fromUserName,
                       'fromUserName': toUserName,
                       'createTime': createTime,
                       'msgType': msgType,
                       'content': replyContent,
                       },
                       content_type = 'application/xml'
        )

