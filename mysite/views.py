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



YOUDAO_KEY_FROM = "hanfeng"
YOUDAO_KEY = "692856525"
YOUDAO_DOC_TYPE = "xml"


def handleRequest(request):
    pdb.set_trace()
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    else:
        return None

def checkSignature(request):
	TOKEN = "xiaoxiao"
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

def paraseYouDaoXml(rootElem):
    replyContent = ''
    if rootElem.tag == 'youdao-fanyi':
        for child in rootElem:
            # 错误码
            if child.tag == 'errorCode':
                if child.text == '20':
                    return 'too long to translate\n'
                elif child.text == '30':
                    return 'can not be able to translate with effect\n'
                elif child.text == '40':
                    return 'can not be able to support this language\n'
                elif child.text == '50':
                    return 'invalid key\n'

            # 查询字符串
            elif child.tag == 'query':
                replyContent = "%s%s\n" % (replyContent, child.text)

            # 有道翻译
            elif child.tag == 'translation': 
                replyContent = '%s%s\n%s\n' % (replyContent, '-' * 3 + u'有道翻译' + '-' * 3, child[0].text)

            # 有道词典-基本词典
            elif child.tag == 'basic': 
                replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'基本词典' + '-' * 3)
                for c in child:
                    if c.tag == 'phonetic':
                        replyContent = '%s%s\n' % (replyContent, c.text)
                    elif c.tag == 'explains':
                        for ex in c.findall('ex'):
                            replyContent = '%s%s\n' % (replyContent, ex.text)

            # 有道词典-网络释义
            elif child.tag == 'web': 
                replyContent = "%s%s\n" % (replyContent, '-' * 3 + u'网络释义' + '-' * 3)
                for explain in child.findall('explain'):
                    for key in explain.findall('key'):
                        replyContent = '%s%s\n' % (replyContent, key.text)
                    for value in explain.findall('value'):
                        for ex in value.findall('ex'):
                            replyContent = '%s%s\n' % (replyContent, ex.text)
                    replyContent = '%s%s\n' % (replyContent,'--')
    return replyContent


class WeixinInterfaceView(View):
    def get(self, request):
        #得到GET内容
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
        pdb.set_trace()
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
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response

    def post(self, request):
        pdb.set_trace()
        msg = parse_msg(request)      #进行xml解析
        queryStr = msg.get('Content','You have input nothing~')
        query_data = {'keyfrom':'hanfeng', 'key':'692856525', 'type':'data', 'doctype':'xml', 'version':'1.1', 'q':queryStr}
        result = requests.get("http://fanyi.youdao.com/openapi.do", params=query_data)
        pass


