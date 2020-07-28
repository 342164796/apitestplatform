#!/usr/bin/python
# coding:utf-8
import requests
import json
class ding():
    def __init__(self,dingUrl,text):
        self.dingUrl=dingUrl
        self.text = text
        self.header = {"Content-Type":"application/json"}
        self.message = """{
    "msgtype": "link", 
    "link": {
        "text": "%s", 
        "title": "【接口报警】", 
        "picUrl": "", 
        "messageUrl": "http://172.18.128.192:8000/base/monapi/"
    }
}"""
    def postmessage(self):
        message = self.message % self.text
        message=message.encode("utf-8")
        print(message)
        r = requests.post(self.dingUrl,data=message,headers=self.header)
        print(r.text)
