import socket
from websocket import create_connection, WebSocket
from time import sleep
import json
header = {
    "X-Iotnd-APIKey":"AQEAAAABAAD_rAp4DJh05a1HAwFT3A6K"
}
hi = """{"hi":{"id":"433a5e84-a2a5-4454-b72c-fd885c2346c4","dev":"E293BB99F918B00ACC03FA6DAFB1E1A5","platf":"tmallgenie","ver":"0.9"}}"""

login = """{"login":{"device_id":"27a1ba8861f10b34bde929df3d2efa1b","id":"888888","mobile":"18765904528","platform":"android","scheme":"basic","secret":"MTg3NjU5MDQ1Mjg6d2MxMjM0"}}"""
#cmd = """{"timer":{"id":"1019","scene":{"iots":[{"action":"close","iot_id":"190208900001","params":"{\"mode\":1,\"wins\":0,\"tempture\":0,\"switch\":0}","statusString":"全关"}],"name":"关闭测试窗帘勿动","period":"once","state":true,"time":"2020-06-10 18:00:00","timer_id":0},"scheme":"add"}}"""
ws = create_connection("ws://qtone.zhipinglife.com/v0/channels ",header = header)
#cmd = """{"asr2nlp":{"id":"0095487e-8c96-43cf-9918-176882730053","sentence":"打开卧室空调"}}"""
cmd = """{"asr2nlp":{"sentence":"打开书房空调","id":"3745fb9f-e16f-4657-8e47-806939358801"}}"""
ws.send(hi)
#ws.send(login)
sleep(0.5)
print(type(cmd))
hi = json.loads(hi)
#cmd = json.loads()
# print('cwd',cwd)
ws.send(cmd)
while True:
    res = ws.recv()
    print(res)
    # if "1005" in res:
    #     ws.close()
    #     break

# dict_data = eval(cwd)
# print(dict_data)
# for k , v in dict_data.items():
#     if k == "id":
#         print(k,v)
#     else:
#         if isinstance(v,dict):
#             for k ,s in v.items():
#                 if k == "id":
#                     print(s)

# import re
# expel = []
# d="{'a':None,'b':None,'c':None,'abc':None}"
# for k in d:
#     expel.append(k)
# a = """{"timer":"{\"scheme\":\"del\",\"id\":\"1016\",\"timer_id\":91,\"$scene\":{\"timer_id\":$/ctrl/params/timers/-1/Id}}"}"""
# #dd = r'\$(.+)\}|,|:'
# dd = r'\$(.+?)[\},:"]'
# #dd = ("(?:isu)\$(?:"+(("|").join(expel))+")")
# L = re.sub(dd,91,a)
# print(L)