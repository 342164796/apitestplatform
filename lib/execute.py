#!/usr/bin/python
# coding:utf-8

from base.models import Project, Sign, Environment, Interface, Case
import requests
import hashlib
import re
import json
from lib import webs
from lib.signtype import get_sign

class Execute():
    def __init__(self, case_id, env_id):
        self.case_id = case_id
        self.env_id = env_id
        self.prj_id, self.env_url, self.private_key = self.get_env(self.env_id)
        self.sign_type = self.get_sign(self.prj_id)


        self.extract_dict = {} #参数名称和值列表
        self.extract = {} #参数和参数路径列表

        self.glo_var = {}
        self.step_json = []
        
        self.content = ""

    def run_case(self):
        case = Case.objects.get(case_id=self.case_id)
        try:
            step_list = eval(case.content)
        except:
            step_list = json.loads(case.content)
        case_run = {"case_id": self.case_id, "case_name": case.case_name, "result": "pass"}
        case_step_list = []
        for step in step_list:
            step_info = self.step(step)
            case_step_list.append(step_info)
            if step_info["result"] == "fail":
                case_run["result"] = "fail"
                break
            if step_info["result"] == "error":
                case_run["result"] = "error"
                break
        case_run["step_list"] = case_step_list
        return case_run




    def step(self, step_content):
        print('setp_content',step_content)
        if_id = step_content["if_id"]
        interface = Interface.objects.get(if_id=if_id)
        var_list = self.extract_variables(step_content)
      #  检查是否存在变量
        if var_list:
            for var_name in var_list:
                var_value = self.get_param(var_name, step_content)

                if var_value is None:
                    var_value = self.get_param(var_name, self.step_json)
                if var_value is None:
                    try:
                        var_value = self.extract_dict[var_name]
                    except Exception as e:
                        print(e)
        #         step_content = json.loads(self.replace_var(step_content, var_name, var_value))
        if_dict = {"url": interface.url, "header": step_content["header"], "body": step_content["body"]}
        # 签名
        if interface.is_sign:
            if_dict["body"] = get_sign(self.sign_type, if_dict["body"], self.private_key)
        if_dict["url"] = self.env_url + interface.url
        if_dict["if_id"] = if_id
        if_dict["if_name"] = step_content["if_name"]
        if_dict["method"] = interface.method
        if_dict["data_type"] = interface.data_type
        project_id = interface.project_id

        try:
            body = str(if_dict["body"])
            if "$" in str(body):
                regex = r'\$(.+?)[\},:"\']'
                list = re.findall(regex,body)
                print("Relist",list)
                print("extract",self.extract_dict)
                for i in list:
                    if isinstance(self.extract_dict[i],int):
                        body = body.replace("$"+i,"%d",1)
                        body = body %  int(self.extract_dict[i])
                body = body.replace("'{","{")
                body = body.replace("}'","}")
            res = self.call_interface(if_dict["method"], if_dict["url"], if_dict["header"],
                                                 body, if_dict["data_type"],project_id)
            if if_dict["method"] == "websocket":
                try:
                    code = eval(res)["ctrl"]["code"]
                except:
                    code = "200"
                print("code",code)
                if_dict["res_status_code"] = code
                if_dict["res_content"] = res
            else:
                if_dict["res_status_code"] = res.status_code
                if_dict["res_content"] = res.text
        except requests.RequestException as e:
            if_dict["result"] = "Error"
            if_dict["msg"] = str(e)
            return if_dict

        if step_content["extract"]:
            for k,v in step_content["extract"].items():
                self.extract[k] = v
            self.get_extract(step_content["extract"], if_dict["res_content"])
        if step_content["validators"]:
            if_dict["result"], if_dict["msg"] = self.validators_result(step_content["validators"], if_dict["res_content"])
        else:
            if_dict["result"] = "pass"
            if_dict["msg"] = {}
        res = {}
        res['result'] = if_dict['result']
        res['res_status_code'] = if_dict['res_status_code']
        res['msg'] = if_dict['msg']
        return res

    def replace_value(self,body,path,value):
        #根据路径替换路径对应的值
        if isinstance(body,str):
            body = eval(body)
        path_list = path.split("/")
        path_list = [ i for i in path_list if i !='']
        for i in path_list:
            x = "body"

#        body[path] = value
        return body

    def return_path(self,body,key,path):
        if isinstance(body,str):
            body = eval(body)
        if isinstance(body,dict):
            for k,v in body.items():
                if "$" in str(v):
                    path = path + k + "/"
                    if v == key:
                        return path
                    else:
                        ret = self.return_path(v,key,path)
                        if ret is not None:
                            return ret
        elif isinstance(body,list):
            for i in len(body):
                if "$" in str(body[i]):
                    path = path + str(i) + "/"
                    ret = self.return_path(body[i],key,path)
                    if ret is not None:
                        return ret

        else:
            return None

    # 验证结果
    def validators_result(self, validators_list, res):
        msg = ""
        result = ""
        for var_field in validators_list:
            check_filed = var_field["check"]
            expect_filed = var_field["expect"]
            testmethod = var_field["comparator"]
            check_filed_value = str(self.get_param(check_filed, res))
            expect_filed = str(expect_filed).replace('\\','').strip()
            try:
             #  check_filed_value = check_filed_value.replace('\n','')
                check_filed_value = check_filed_value.replace('\\n','')
                check_filed_value = check_filed_value.replace('\\','').strip()
                check_filed_value = check_filed_value.replace("'", '"')
            except Exception as e:
                print(e)
            if testmethod == 'eq':
               # print("ssss",check_filed_value,expect_filed)
                if check_filed_value == expect_filed:
                    result = "pass"
                    msg = ""
                elif "|" in expect_filed:
                    expect_list = expect_filed.split("|")
                    if check_filed_value in expect_list:
                        result = "pass"
                        msg = ""
                   # print(expect_list)
                else:
                    result = "fail"
                    msg = "字段: " + check_filed + " 实际值为：" + str(check_filed_value) + " 与期望值：" + expect_filed + " 不符"
                    break
            elif testmethod == 'startswith':
                if check_filed_value.startswith(expect_filed):
                    result = "pass"
                    msg = ""
                else:
                    result = "fail"
                    msg = "字段: " + check_filed + " 实际值为: " + str(check_filed_value) + "与startswith期望值: " + expect_filed + " 不符"
                    break
            elif testmethod == 'endswith':
                if check_filed_value.endswith(expect_filed):
                    result = "pass"
                    msg = ""
                else:
                    result = "fail"
                    msg = "字段: " + check_filed + " 实际值为: " + str(check_filed_value) + "与endswith期望值: " + expect_filed + " 不符"
                    break
            elif testmethod == "no equal":
                if check_filed_value != expect_filed:
                    result = "pass"
                    msg = ""
                else:
                    result = "fail"
                    msg = "字段: " + check_filed + " 实际值为：" + str(check_filed_value) + " 与期望值no equal：" + expect_filed + " 不符"
                    break
        return result, msg

    # 在response中提取参数, 并放到列表中
    def get_extract(self, extract_dict, res):
        for key, value in extract_dict.items():
            key = key.replace('$','')
            key_value = self.get_param(value, res)
          #  key = '$'+key
            self.extract_dict[key] = key_value
            print("extract",self.extract_dict)




    # 替换内容中的变量, 返回字符串型
    def replace_var(self, content, var_name, var_value):
        if not isinstance(content, str):
            content = json.dumps(content)
        var_name = "$" + var_name
        content = content.replace(str(var_name), str(var_value))
        return content



    # 从内容中提取所有变量名, 变量格式为$variable,返回变量名list
    def extract_variables(self, content):
        variable_regexp = r"\$([\w_]+)"
        if not isinstance(content, str):
            content = str(content)
        try:
            return re.findall(variable_regexp, content)
        except TypeError:
            return []

    # 在内容中获取某一参数的值
    def get_param(self, param, content):
        if param.startswith('/'):
            return self.get_param_from_path(param,content)
        param_val = None
        if isinstance(content, str):
            # content = json.loads(content)
            try:
                content = json.loads(content)
            except:
                content = ""
        if isinstance(content, dict):
            param_val = self.get_param_reponse(param, content)
        if isinstance(content, list):
            dict_data = {}
            for i in range(len(content)):
                try:
                    dict_data[str(i)] = eval(content[i])
                except:
                    dict_data[str(i)] = content[i]
            param_val = self.get_param_reponse(param, dict_data)
        if param_val is None:
            return param_val
        else:
            if "$" + param == param_val:
                param_val = None
            return param_val
# 按照路径取值
    def get_param_from_path(self,param,content):
        path_list = param.split('/')
        for i in path_list:
            if i == "":
                path_list.remove(i)
        self.content = content
        for param in path_list:
            value = self.get_param_from_response(param)
        return value
    def get_param_from_response(self,param):
        content = self.content
        if isinstance(content,str):
            try:
                content = json.loads(content)
            except:
                content=""
        if isinstance(content,dict):
            try:
                self.content = content[param]
                return self.content
            except:
                self.content=""
                return self.content
        if isinstance(content,list):
            param = int(param)
            self.content = content[param]
            return self.content
        
    def get_param_reponse(self, param_name, dict_data, default=None):
        for k, v in dict_data.items():
          #  print(k, v)
            if k == param_name:

                return v
            else:
                if isinstance(v, dict):
                    ret = self.get_param_reponse(param_name, v)
                    if ret is not default:
                        return ret
                if isinstance(v, list):
                    for i in v:
                        if isinstance(i, dict):
                            ret = self.get_param_reponse(param_name, i)
                            if ret is not default:
                                return ret
                        else:
                            pass
        return default



    # 获取测试环境
    def get_env(self, env_id):
        env = Environment.objects.get(env_id=env_id)
        prj_id = env.project.prj_id
        return prj_id, env.url, env.private_key

    # 获取签名方式
    def get_sign(self, prj_id):
        """
        sign_type: 签名方式
        """
        prj = Project.objects.get(prj_id=prj_id)
        sign_type = prj.sign.sign_id
        return sign_type


    # 发送请求
    def call_interface(self, method, url, header, data, content_type='json',project_id = None):
        try:
            data = str(data).replace('\\n', '').replace('\\t','')
            data = eval(data)
        except:
            data = data
        if method == "post":
            if content_type == "json":
                for k,v in data.items():
                    if "[" in v:
                        data[k] = json.loads(v.strip())
                res = requests.post(url=url, json=data, headers=header, verify=False)
            if content_type == "data":
                res = requests.post(url=url, data=data, headers=header, verify=False)
        if method == "get":
            print(url,data)
            res = requests.get(url=url, params=data, headers=header, verify=False)
        if method == "websocket":
           # cwd = """{"login":{"device_id":"251883de833a9e8e1d09b0c0928a9c3d","id":"1005","mobile":"18765904528","platform":"android","scheme":"basic","secret":"MTg3NjU5MDQ1Mjg6d2MxMjM0"}}"""
            data = json.dumps(data,separators=(',',':'))
            res = webs.main(url, data, header,project_id)
            print("res###############",res)
            return res
        #return res

    def get_body(self,data):
        #把data转成uri
        uri = '?'
        keys = data.keys()
        for i in keys:
            string = i + '=' + data[i] + '&'
            uri = uri + string
        uri = uri[:-1]
        return uri