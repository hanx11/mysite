# -*- coding:utf-8 -*-

from django.http import HttpResponse
import hashlib

def handleRequest(request):
    if request.method == 'GET':
        response = HttpResponse(checkSignature(request), content_type="text/plain")
        return response
    else:
    	return None

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

