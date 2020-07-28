# -*- coding: utf-8 -*-
from django.shortcuts import render
from base.models import Project, Sign, Environment, Interface, Case, Plan, Report, MonProject,MonApi,MonCfg
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib import messages
from django.core import serializers
from lib.execute import Execute
from lib.monapi import monMain,alert
import time
import json
import requests
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
# Create your views here.



# 项目增删改查
def project_index(request):
    prj_list = Project.objects.all()
    return render(request, "base/project/index.html", {"prj_list": prj_list})


def project_add(request):
    if request.method == 'POST':
        prj_name = request.POST['prj_name']
        name_same = Project.objects.filter(prj_name=prj_name)
        if name_same:
            return HttpResponse("该项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign']
            sign = Sign.objects.get(sign_id=sign_id)
            prj = Project(prj_name=prj_name, description=description, sign=sign)
            prj.save()
            return HttpResponseRedirect("/base/project/")
    sign_list = Sign.objects.all()
    return render(request, "base/project/add.html", {"sign_list": sign_list})

def project_update(request):
    if request.method == 'POST':
        prj_id = request.POST['prj_id']
        prj_name = request.POST['prj_name']
        name_exit = Project.objects.filter(prj_name=prj_name).exclude(prj_id=prj_id)
        if name_exit:
            # messages.error(request, "项目已存在")
            return HttpResponse("项目已存在")
        else:
            description = request.POST['description']
            sign_id = request.POST['sign_id']
            sign = Sign.objects.get(sign_id=sign_id)
            Project.objects.filter(prj_id=prj_id).update(prj_name=prj_name, description=description,sign=sign)
            return HttpResponseRedirect("/base/project/")
    prj_id = request.GET['prj_id']
    prj = Project.objects.get(prj_id=prj_id)
    sign_list = Sign.objects.all()
    return render(request, "base/project/update.html", {"prj": prj, "sign_list": sign_list})

def project_delete(request):
    if request.method == 'GET':
        prj_id = request.GET['prj_id']
        Project.objects.filter(prj_id=prj_id).delete()
        return HttpResponseRedirect("base/project/")



# 加密方式增删改查
def sign_index(request):
    sign_list = Sign.objects.all()
    return render(request, "system/sign_index.html", {"sign_list": sign_list})

def sign_add(request):
    if request.method == 'POST':
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        sign = Sign(sign_name=sign_name, description=description)
        sign.save()
        return HttpResponseRedirect("/base/sign/")
    return render(request, "system/sign_add.html")

# 更新加密方式
def sign_update(request):
    if request.method == 'POST':
        sign_id = request.POST['sign_id']
        sign_name = request.POST['sign_name']
        description = request.POST['description']
        Sign.objects.filter(sign_id=sign_id).update(sign_name=sign_name, description=description)
        return HttpResponseRedirect("/base/sign/")
    sign_id = request.GET['sign_id']
    sign = Sign.objects.get(sign_id=sign_id)
    return render(request, "system/sign_update.html", {"sign": sign})
# 加密方式删除
def sign_delete(request):
    sign_id = request.GET['sign_id']
    Sign.objects.filter(sign_id=sign_id).delete()
    return HttpResponseRedirect("/base/sign/")

# 测试环境增删改查
def env_index(request):
    env_list = Environment.objects.all()
    return render(request, "base/env/index.html", {"env_list": env_list})

def env_add(request):
    if request.method == 'POST':
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        env = Environment(env_name=env_name, url=url, project=project,
                           private_key=private_key, description=description)
        env.save()
        return HttpResponseRedirect("/base/env/")
    prj_list = Project.objects.all()
    return render(request, "base/env/add.html", {"prj_list": prj_list})
# 测试环境更新
def env_update(request):
    if request.method == 'POST':
        env_id = request.POST['env_id']
        env_name = request.POST['env_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        private_key = request.POST['private_key']
        description = request.POST['description']
        Environment.objects.filter(env_id=env_id).update(env_name=env_name, url=url, project=project, private_key=private_key, description=description)
        return HttpResponseRedirect("/base/env/")
    env_id = request.GET['env_id']
    env =Environment.objects.get(env_id=env_id)
    prj_list = Project.objects.all()
    return render(request, "base/env/update.html", {"env": env, "prj_list": prj_list})
#删除测试环境
def env_delete(request):
    env_id = request.GET['env_id']
    Environment.objects.filter(env_id=env_id).delete()
    return HttpResponseRedirect("/base/env/")

# 接口增删改查
def interface_index(request):
    if_list = Interface.objects.all()
    return render(request, "base/interface/index.html", {"if_list": if_list})

def interface_add(request):
    if request.method == 'POST':
        if_name = request.POST['if_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_data = request.POST['request_header_data']
        request_body_data = request.POST['request_body_data']
        response_header_data = request.POST['response_header_data']
        response_body_data = request.POST['response_body_data']
        interface = Interface(if_name=if_name, url=url, project=project, method=method, data_type=data_type,
                          is_sign=is_sign, description=description, request_header_param=request_header_data,
                          request_body_param=request_body_data, response_header_param=response_header_data,
                          response_body_param=response_body_data)
        interface.save()
        return HttpResponseRedirect("/base/interface/")
    prj_list = Project.objects.all()
    return render(request, "base/interface/add.html", {"prj_list": prj_list})

#删除接口
def interface_delete(request):
    if_id = request.GET['if_id']
    Interface.objects.filter(if_id=if_id).delete()
    return HttpResponseRedirect("/base/interface/")
#编辑接口
def interface_update(request):
    if request.method == 'POST':
        print(request.POST)
        if_id = request.POST['if_id']
        if_name = request.POST['if_name']
        url = request.POST['url']
        method = request.POST['method']
        data_type = request.POST['data_type']
        is_sign = request.POST['is_sign']
        description = request.POST['description']
        request_header_param = request.POST['request_header_data']
        request_body_param = request.POST['request_body_data']
        response_header_param = request.POST['response_header_data']
        response_body_param = request.POST['response_body_data']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        Interface.objects.filter(if_id=if_id).update(if_name=if_name,url=url,method=method,data_type=data_type,is_sign=is_sign,description=description,
                                                     request_header_param=request_header_param,request_body_param=request_body_param,
                                                     response_header_param=response_header_param,response_body_param=response_body_param,project=project)
        return HttpResponseRedirect("/base/interface/")
    if_id = request.GET['if_id']
    if_list = Interface.objects.get(if_id=if_id)
    prj_list = Project.objects.all()
    if_list.request_header_param = json.loads(if_list.request_header_param)
    if_list.request_body_param = json.loads(if_list.request_body_param)
    if_list.response_header_param = json.loads(if_list.response_header_param)
    if_list.response_body_param = json.loads(if_list.response_body_param)
    return render(request, "base/interface/update2.html", {"if": if_list,"prj_list":prj_list})
# 接口增删改查
def case_index(request):
    case_list = Case.objects.all().order_by('-case_id')
    prj_list = Project.objects.all()
    paginator = Paginator(case_list,50)
    page = request.GET.get('page')
    try:
        case_list = paginator.page(page)
    except PageNotAnInteger:
        case_list = paginator.page(1)
    except InvalidPage:
        return HttpResponse("找不到页面内容")
    except EmptyPage:
        case_list = paginator.page(paginator.num_pages)
    return render(request, "base/case/index.html", {"case_list": case_list,"prj_list":prj_list})
def case_search(request):
    prj_list = Project.objects.all()
    q = request.GET.get('q')
    p = request.GET.get('p')
    #prjName 返回给前端的值
    if p == "":
        prjName = ''
        case_list = Case.objects.filter(case_name__contains=q)
    else:
        prjName = Project.objects.filter(prj_id=p).first()
        case_list = Case.objects.filter(case_name__contains=q).filter(project_id=p)

    paginator = Paginator(case_list,50)
    page = request.GET.get('page')
    if not page:
        page = 1
    try:
        case_list = paginator.page(page)
    except InvalidPage:
        return HttpResponse("找不到页面内容")
    except EmptyPage:
        case_list = paginator.page(paginator.num_pages)
    return render(request, "base/case/index.html", {"case_list": case_list,"prj_list":prj_list,"q":q,"p":prjName})
def case_add(request):
    if request.method == 'POST':
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        case = Case(case_name=case_name, project=project, description=description, content=content)
        case.save()
        return HttpResponseRedirect("/base/case/")
    prj_list = Project.objects.all()
    return render(request, "base/case/add.html", {"prj_list": prj_list})
#用例删除
def case_delete(request):
    case_id = request.GET['case_id']
    Case.objects.filter(case_id=case_id).delete()
    return HttpResponseRedirect("/base/case/")
#用例编辑
def case_update(request):
    if request.method == 'POST':
        print("POST",request.POST)
        case_id = request.POST['case_id']
        case_name = request.POST['case_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        description = request.POST['description']
        content = request.POST['content']
        Case.objects.filter(case_id=case_id).update(case_name=case_name,project=project,description=description,content=content)
        return HttpResponseRedirect("/base/case/")
    case_id = request.GET['case_id']
    case = Case.objects.get(case_id=case_id)
    prj_list = Project.objects.all()
    case.content = json.loads(case.content)
    try:
        if_id = case.content[0]['if_id']
        case.if_id = if_id
        case.interface = Interface.objects.get(if_id=if_id)
    except Exception as e:
        print(e)
    aaa = Case.objects.filter(case_id=case_id).values()
    print(aaa)
    return render(request, "base/case/update.html",{"case":case,"prj_list":prj_list,'aaa':aaa})
    
def case_run(request):
    if request.method == 'POST':
        print(request.POST)
        case_id = request.POST['case_id']
        env_id = request.POST['env_id']
        execute = Execute(case_id, env_id)
        case_result = execute.run_case()
        return JsonResponse(case_result)


# 计划增删改查
def plan_index(request):
    plan_list = Plan.objects.all()
    return render(request, "base/plan/index.html", {"plan_list": plan_list})

def plan_add(request):
    if request.method == 'POST':
        plan_name = request.POST['plan_name']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env_id = request.POST['env_id']
        environment = Environment.objects.get(env_id=env_id)
        description = request.POST['description']
        content = request.POST.getlist("case_id")
        plan = Plan(plan_name=plan_name, project=project, environment=environment, description=description, content=content)
        plan.save()
        return HttpResponseRedirect("/base/plan/")
    prj_list = Project.objects.all()
    return render(request, "base/plan/add.html", {"prj_list": prj_list})

def plan_update(request):
    
    if request.method == 'POST':
        print(request.POST)
        plan_id = request.POST['plan_id']
        plan_name = request.POST['plan_name']
        description = request.POST['description']
        content = request.POST.getlist('case_id')
        environment_id = request.POST['env_id']
        prj_id = request.POST['prj_id']
        project = Project.objects.get(prj_id=prj_id)
        env = Environment.objects.get(env_id=environment_id)
        print(request.POST.getlist('case_id'))
        print('content',type(content))
        Plan.objects.filter(plan_id=plan_id).update(plan_name=plan_name,description=description,content=content,environment=env,project=project)
        return HttpResponseRedirect("/base/plan/")
    plan_id = request.GET['plan_id']
    plan = Plan.objects.get(plan_id=plan_id)
    prj_list = Project.objects.all()
    environment = Project.objects.all()
    project_id = plan.project_id
    env_list = Environment.objects.filter(project_id=project_id)
    return render(request, "base/plan/update2.html",{"plan": plan,"prj_list":prj_list,"env_list":env_list,'environment':environment})

def plan_delete(request):
    plan_id = request.GET['plan_id']
    Plan.objects.filter(plan_id=plan_id).delete()
    return HttpResponseRedirect("/base/plan/")
def plan_run(request):
    print("begin start test plan !!!")
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = Plan.objects.get(plan_id=plan_id)
        env_id = plan.environment.env_id
        case_id_list = eval(plan.content)
        case_num = len(case_id_list)
        content = []
        pass_num = 0
        fail_num = 0
        error_num = 0
        for case_id in case_id_list:
            execute = Execute(case_id, env_id)
            case_result = execute.run_case()
            content.append(case_result)
            if case_result["result"] == "pass":
                pass_num += 1
            if case_result["result"] == "fail":
                fail_num += 1
            if case_result["result"] == "error":
                error_num += 1
        report_name = plan.plan_name + "-" + time.strftime("%Y%m%d%H%M%S")
        # if Report.objects.filter(plan=plan):
        #     Report.objects.filter(plan=plan).update(report_name=report_name, content=content, case_num=case_num,
        #                                             pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        if Report.objects.filter(report_name=report_name):
            Report.objects.filter(plan=plan).update(report_name=report_name, content=content, case_num=case_num,
                                                         pass_num=pass_num, fail_num=fail_num, error_num=error_num)
        else:
            report = Report(plan=plan, report_name=report_name, content=content, case_num=case_num,
                            pass_num=pass_num, fail_num=fail_num, error_num=error_num)
            report.save()
        return HttpResponse(plan.plan_name + " 执行成功！")


def report_index(request):
    plan_id = request.GET['plan_id']
    report_list = Report.objects.filter(plan_id=plan_id).order_by('-report_id')
    # report_content = eval(report.content)
   # return render(request, "report.html", {"report": report, "report_content": report_content})
    return render(request,"index.html",{"report_list":report_list})

def report_detail(request):
    report_id = request.GET['report_id']
    report = Report.objects.get(report_id=report_id)
    report_content = eval(report.content)
    return render(request, "report.html", {"report": report, "report_content":report_content})
def findata(request):
    if request.method == 'POST':
        pass
    if request.method == 'GET':
        get_type = request.GET["type"]
        if get_type == "get_all_if_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 返回字典列表
            if_list = Interface.objects.filter(project=prj_id).all().values()
            # list(if_list)将QuerySet转换成list
            return JsonResponse(list(if_list), safe=False)
        if get_type == "get_if_by_if_id":
            if_id = request.GET["if_id"]
            # 查询并将结果转换为json
            interface = Interface.objects.filter(if_id=if_id).values()
            return JsonResponse(list(interface), safe=False)
        if get_type == "get_env_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Environment.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
        if get_type == "get_all_case_by_prj_id":
            prj_id = request.GET["prj_id"]
            # 查询并将结果转换为json
            env = Case.objects.filter(project_id=prj_id).values()
            return JsonResponse(list(env), safe=False)
        if get_type == 'get_case_by_case_id':
            case_id = request.GET['case_id']
            case = Case.objects.filter(case_id=case_id).values()
            return JsonResponse(list(case), safe=False)
        if get_type == 'get_case_content_by_case_id':
            case_id = request.GET['case_id']
            querry_content = Case.objects.filter(case_id=case_id).values('content')
            content = querry_content[0]['content']
            return JsonResponse(json.loads(content), safe=False)
        if get_type == "get_plan_by_plan_id":
            plan_id = request.GET['plan_id']
            plan = Plan.objects.filter(plan_id=plan_id).values()
            return JsonResponse(list(plan), safe=False)
def moncfg(request):
    prj_list = MonProject.objects.all()
    return render(request, "base/mon/moncfg.html",{"prj_list":prj_list})

def mon_add(request):
    if request.method == "GET":
        return render(request, "base/mon/mon_add.html")
    else:
        name = request.POST['prj_name']
        interview_time = request.POST['interview_time']
        monproject = MonProject(monprj_name = name, interview_time = interview_time)
        monproject.save()
        return HttpResponseRedirect("/base/moncfg/")
def mon_update(request):
    if request.method == 'POST':
        monprj_id = request.POST['monprj_id']
        monprj_name = request.POST['monprj_name']
        name_exit = MonProject.objects.filter(monprj_name=monprj_name).exclude(monprj_id=monprj_id)
        if name_exit:
            # messages.error(request, "项目已存在")
            return HttpResponse("项目已存在")
        else:
            MonProject.objects.filter(monprj_id=monprj_id).update(monprj_name=monprj_name)
            return HttpResponseRedirect("/base/moncfg/")
    monprj_id = request.GET['monprj_id']
    monprj = MonProject.objects.get(monprj_id=monprj_id)
    return render(request, "base/mon/monupdate.html", {"prj": monprj})


def mon_delete(request):
    monprj_id = request.GET['monprj_id']
    MonProject.objects.filter(monprj_id=monprj_id).delete()
    return HttpResponseRedirect("/base/moncfg/")

def monapi(request):
    monapi_list = MonApi.objects.all()
    # print(monapi_list[0].time)
    return render(request, "base/api/index.html",{"monapi_list":monapi_list})

def monapi_add(request):
    if request.method == "POST":
        content={}
        try:
            name = request.POST['name']
            monprj_id = request.POST['monprj_id']
            content["method"] = request.POST['method']
            content["api"] = request.POST['api']
            content["header"] = request.POST['header']
            content["body"] = request.POST['body']
            content["checks"] = request.POST['checks']

            monapi = MonApi(name=name,content=content,monprj_id=monprj_id)
            monapi.save()
        except:
            return HttpResponse("缺少必要参数！")
        return HttpResponseRedirect("base/monapi/")
    monprj = MonProject.objects.all()
    return render(request,"base/api/add.html",{"prj_list": monprj})
def monapi_delete(request):
    id = request.GET['id']
    MonApi.objects.filter(id=id).delete()
    return HttpResponseRedirect("/base/monapi/")

def monapi_update(request):
    if request.method == 'POST':
        try:
            content = {}
            id = request.POST['id']
            name = request.POST['name']
            monprj_id = request.POST['monprj_id']
            content["method"] = request.POST['method']
            content["api"] = request.POST['api']
            content["header"] = request.POST['header']
            content["body"] = request.POST['body']
            content["checks"] = request.POST['checks']
            MonApi.objects.filter(id=id).update(name=name,content=content,monprj_id=monprj_id)
            return HttpResponseRedirect("/base/monapi/")
        except:
            return HttpResponse("缺少必要参数！")
    id = request.GET['id']
    res = MonApi.objects.get(id=id)
    api = {}
    api['id'] = id
    api['name'] = res.name
    content = eval(res.content)
    api['api'] = content['api']
    api['header'] = content['header']
    api['body'] = content['body']
    api['checks'] = content['checks']
    api['method'] = content['method']
    api['monprj_id'] = res.monprj_id
    api['monprj_name'] = MonProject.objects.get(monprj_id = res.monprj_id)
    monprj_list = MonProject.objects.all()
    return render(request,"base/api/update.html",{"api":api,"monprj_list":monprj_list})

def monapi_run(request):
    id = request.GET['id']
    content = MonApi.objects.get(id=id).content
    status, response_time, details = monMain(content)
    MonApi.objects.filter(id=id).update(status=status,time=response_time,details = details)
    # alert()
    return HttpResponseRedirect("/base/monapi/")

def msgcfg(request):
    msgcfg_list = MonCfg.objects.all()
    return render(request,"base/msgcfg/index.html",{"msgcfg_list":msgcfg_list})

def msgcfg_update(request):
    if request.method == "POST":
        id = request.POST['id']
        ding = request.POST['ding']
        jingmoqi = request.POST['jingmoqi']
        MonCfg.objects.filter(id=id).update(ding=ding,jingmoqi=jingmoqi)
        return HttpResponseRedirect('/base/msgcfg/')
    id = request.GET['id']
    moncfg = MonCfg.objects.get(id=id)
    return render(request,"base/msgcfg/update.html",{"moncfg":moncfg})


#监控定时任务入口
def task():
    url = "http://127.0.0.1:8000/base/monapi_run/?id=%d"
    api_list = MonApi.objects.all()
    for api in api_list:
        id = api.id
        r = requests.get(url % id)
        time.sleep(0.5)
    #是否报警入口
    alert()
    return
