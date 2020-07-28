import requests
import json
d = {'senderId': '0452aab6f4173de58c1d9bf73a54439d', 'apkVersions': [{"packageName": "com.taobao.tv.smartpad","versionCode": 1200}, {"packageName": "com.taobao.tv.iotagent","versionCode": 10302}]}

url = 'http://zuul-test.zhipinglife.com/service/parameter-server/api/v4/parameter/remoterConfig/selfUpgrade'

r = requests.post(url=url,json=d)
print(r.text)