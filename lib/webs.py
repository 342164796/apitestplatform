# encoding: utf-8
import websocket
import json
import time

production_hi = """{"hi":{"id":"1001","ver":"0.2.1","token":"AqXN8VZ3YsI8lMtxEZQaqnX-vZV_34qSdXorLO1eqzuN","dev":"251883de833a9e8e1d09b0c0928a9c3d","platf":"android"}}"""
hi = """{"hi":{"id":"1001","ver":"0.2.1","token":"AqXN8VZ3YsI8lMtxEZQaqnUwyuYZN2hxEAIsocYEIpV8","dev":"251883de833a9e8e1d09b0c0928a9c3d","platf":"android"}}"""
login = """{"login":{"device_id":"27a1ba8861f10b34bde929df3d2efa1b","id":"888888","mobile":"18765904528","platform":"android","scheme":"basic","secret":"MTg3NjU5MDQ1Mjg6d2MxMjM0"}}"""
#login = """{"login":{"apns":"AqXN8VZ3YsI8lMtxEZQaqnX-vZV_34qSdXorLO1eqzuN","device_id":"251883de833a9e8e1d09b0c0928a9c3d","id":"1001","mobile":"13824299656","platform":"android","scheme":"basic","secret":"MTM4MjQyOTk2NTY6d2MxMjM0"}}"""
def main(url,data,header,project_id):
    try:
        ws = websocket.create_connection(url,header=header)
    except Exception as e:
        print(e)
        return None
    #自动化测试
    if project_id == 9:
        print("test")
        ws.send(hi)
        ws.send(login)
        time.sleep(0.5)
        ids = get_id(data)
        print("send websocket data ",data)
        ws.send(data)
        endtime = int(round(time.time())) + 5
        while True:
            nowTime = int(round(time.time()))
            print(nowTime,endtime)
            if nowTime <= endtime:
                res = ws.recv()
                id = '"id":"%s"' %ids
                print(id)
                if str(id) in res:
                    ws.close()
                    print("websocket is closed!")
                    return res

            else:
                return None
        ws.close()
        return None
    #监控
    elif project_id == 8:
        print("monitor")
        datas = data.split('\n')
        datas.insert(0,production_hi)
        print(datas)
        for data in datas:
            ids = get_id(data)
            if "iot_ac" in data:  #判断发送消息是否空调控制
                id = '"act":"ac_status"'
            else:
                id = '"id":"%s"' % ids
            print("send data " + data)

            ws.send(data)
            starttime = int(time.time() * 1000)
            timeout = int(round(time.time())) + 20
            while True:
                nowtime = int(round(time.time()))
                if nowtime <= timeout:
                    res = ws.recv()
                    print("res: " + res)
                    if str(id) in res:
                        endtime = int(time.time() * 1000)
                        if data != datas[-1]:
                            print("continue")
                            break
                        else:
                            ws.close()
                            print("return")
                            responsetime = endtime - starttime
                            return res,responsetime
                else:
                    ws.close()
                    return None,None
        # for data in datas:
        #     print("send data "+data)
        #     ws.send(data)
        #     if data == datas[-1]:
        #         startTime = int(time.time() * 1000)
        #     else:
        #         print("sleep")
        #         time.sleep(0.1)


        # while True:
        #     nowTime = int(round(time.time()))
        #     if nowTime <= endtime:
        #         res = ws.recv()
        #         print(res)
        #         id = '"id":"%s"' %ids
        #         if str(id) in res:
        #             endTime = int(time.time() * 1000)
        #             ws.close()
        #             t = endTime - startTime
        #             return res,t
        #     else:
        #         ws.close()
        #         return None,None
        # ws.close()
        # return None,None

def get_id(data,default=None):
    if not isinstance(data,dict):
        try:
            data = eval(data)
        except:
            data = json.loads(data)
    print(data)
    try:
        for k , v in data.items():
            if k == "id":
                return v
            else:
                if isinstance(v,dict):
                    ret = get_id(v)
                    if ret is not default:
                        return ret
    except:
        return None



if __name__ == "__main__":
    url ="ws://qtone-test.zhipinglife.com/v0/channels"
    header = {"X-Iotnd-APIKey":"AQEAAAABAAD_rAp4DJh05a1HAwFT3A6K"}
   # cwd = """{"login":{"device_id":"251883de833a9e8e1d09b0c0928a9c3d","id":"1005","mobile":"18765904528","platform":"android","scheme":"basic","secret":"MTg3NjU5MDQ1Mjg6d2MxMjM0"}}"""
    cwd = """{'login': '{"device_id":"e47288ec98840d61afe77a98bfe91b83","id":"1002","mobile":"18765904528","platform":"android","scheme":"basic","secret":"MTg3NjU5MDQ1Mjg6d2MxMjM0"}'}"""
    main(url,cwd,header)
    # ws = websocket.WebSocketApp(url,header = header,
    #                             on_message = on_message,
    #                             on_error = on_error,
    #                             on_close = on_close)
    # ws.on_open = on_open
    # ws.run_forever()