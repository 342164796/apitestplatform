#!/usr/bin/python
# coding:utf-8
import requests
from base.models import MonApi,Alert,MonCfg
import json
import time
from lib import webs,execute,ding
def monMain(content):
    content = eval(content)
    api = content['api']
    method = content['method']
    header = json.loads(content['header'])
    body = content['body']
    checks = content['checks']
    details = ""
    if method == "websocket":
        res,response_time = webs.main(api,body,header,8)
    if res == None or response_time == None:
        status = 0
        details = "接口访问错误或超时"
        return status,response_time,details
    if checks:
        res = json.loads(res)
        try:
            checks = eval(checks)
        except Exception as e:
            details = "校验数据格式化错误: " + str(e)
            return 0,response_time, details
        keys = checks.keys()
        result = []
        for key in keys:
            trueValue = getValueFromResponse(key,res)
            r = checkValue(key,checks[key],trueValue)
            result.append(r)
        for i in result:
            if i != 1:
                return 0,response_time,i
        print(result)
        return 1,response_time,details
    else:
        status = 1
        return status,response_time,details

def getValueFromResponse(key,response,default=None):
    for k,v in response.items():
        if k == key:
            return v
        else:
            if isinstance(v ,dict):
                ret = getValueFromResponse(key,v)
                if ret is not default:
                    return ret
            if isinstance(v,list):
                for i in v:
                    if isinstance(i,dict):
                        ret = getValueFromResponse(key,i)
                        if ret is not default:
                            return ret
                    else:
                        pass
    return default
def checkValue(key,expectValue,TrueValue):
    if expectValue == TrueValue:
        return 1
    else:
        return "%s字段校验错误，预期结果%s,实际结果%s" % (key,str(expectValue),str(TrueValue))


def alert():
    moncfg = MonCfg.objects.get(id=1)
    apiList = MonApi.objects.filter(status=0)
    alerList = Alert.objects.all()
    alertIdList = []
    for alert in alerList:
        alertIdList.append(alert.api_id)
    for api in apiList:
        if api.id not in alertIdList:
            alert = Alert(api_id=api.id,api_name=api.name,alert_details=api.details,alert_time=int(time.time()),isAlert=0,count=1)
            alert.save()
        else:
            count = Alert.objects.get(api_id = api.id).count
            Alert.objects.filter(api_id=api.id).update(count=count+1)

    apiList2 = MonApi.objects.filter(status = 1)
    #检查是否有恢复的接口，如果有的话删除alert数据
    for api in apiList2:
        if api.id in alertIdList:
            isAlert = Alert.objects.get(api_id=api.id).isAlert
            if isAlert == 1:
                #发接口恢复dingding通知
                text = "%s 接口恢复正常" % api.name
                d = ding.ding(moncfg.ding,text)
                d.postmessage()
            Alert.objects.filter(api_id=api.id).delete()
 #发送dingding消息
    postAlerDingMsg(moncfg.ding,moncfg.jingmoqi)


def postAlerDingMsg(dingUrl,jingmoqi):
    alertList = Alert.objects.all()
    for alert in alertList:
        if alert.isAlert == 0 and alert.count >=3:
            #超过失败次数，报警
            _postAlertDingMsg(alert,dingUrl)
        if alert.isAlert == 1 and int(time.time()) > int(alert.alert_time) + jingmoqi:
            #已经报过警了，但是超过了静默期，再报警一次
            _postAlertDingMsg(alert, dingUrl)

    return

def _postAlertDingMsg(alert,dingUrl):
    text = "%s 接口访问错误，\n 错误详情：%s" % (alert.api_name,alert.alert_details)
    print(dingUrl,text)
    d = ding.ding(dingUrl,text)
    d.postmessage()
    Alert.objects.filter(id=alert.id).update(isAlert=1,alert_time=int(time.time()))