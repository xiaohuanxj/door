#!/usr/bin/env python
# coding=utf-8
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from jump.models import idcInfo
from jump import models
import json,requests,logging
from . import  doormath
import random,string,IPy
import sys

HOSTNAME = 'http://osmp.qa-ag.xxqq.com'
logger = logging.getLogger('django')

@csrf_exempt
def apiType(request):
#得到操作类型
    if request.method == 'GET':
        response = {
            "content": [{"apiName":"新增用户","api": HOSTNAME + "/jump/v1/adduser"},
            {"apiName":"删除用户","api": HOSTNAME + "/jump/v1/deluser"},
            {"apiName":"更新用户","api": HOSTNAME + "/jump/v1/updateuser"},
            #{"sel_user":"查询用户","selectuserinterfaces":"jump/v1/adduser"},
            {"apiName":"重置密码", "api": HOSTNAME + "/jump/v1/resetpwd"},
            {"apiName":"临时权限","api": HOSTNAME + "/jump/v1/tmppermission"}],
            "status":"OK",
            "errorMsg": "",
        }
        logger.info(" api /jump/v1/apitype 200 ")
        return JsonResponse(response, safe=False)
    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 GET方法！503")
        return JsonResponse(response, safe=False)

# Create your views here.
@csrf_exempt
def queryIdc(request):
#查询机房信息
    if request.method == 'GET':
        idcList = idcInfo.objects.filter().values("zhName","idcName")
        content = [a for a in idcList]
        response = {
            "content": content,
            "status":"OK",
            "errorMsg": "",
        }
        logger.info(" api /jump/v1/queryidc  200  ")
        return JsonResponse(response, safe=False)
    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 GET方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def getDepartment(request):
#查询部门信息
    departMentlist = []
    departMentrootlist = []
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        Url = 'https://' + ip + '/api/departments'
        headers = {'Content-Type': 'application/json', 'AccessToken': token}
        html=requests.get(url=Url, data=None,headers=headers,verify=False)
        departMentinfo=json.loads(html.text)
        for i in range(len(departMentinfo['departments'])):
            departMentdict = {}
            departmentid = departMentinfo['departments'][i]['departmentId']
            departmentname = departMentinfo['departments'][i]['departmentName']
            departMentdict['departmentId'] = departmentid
            departMentdict['departmentName'] = departmentname
            departMentlist.append(departMentdict)
        for j in range(len(departMentinfo['departments'])):
            departMentrootdict = {}
            if departMentinfo['departments'][j]['departmentName'] == '用户根':
                departmentid = departMentinfo['departments'][j]['departmentId']
                departmentname = departMentinfo['departments'][j]['departmentName']
                departMentrootdict['departmentId'] = departmentid
                departMentrootdict['departmentName'] = departmentname
                departMentrootlist.append(departMentrootdict)
            else:
                pass
        response = {
            "content": departMentrootlist,
            "status":"OK",
            "errorMsg": "",
        }
        logger.info(" %s idcenName: %s ,%s 200 reason:%s  " % (request.method,idcenName,Url,reason))
        return JsonResponse(response, safe=False)

    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def permissionGroup(request):
#查询根部门的权限组信息
    grouplist=[]
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        userName = info.get("userName")
        userDepartmentid = doormath.selectUserdepartmentid(idcenName,userName)
        rootDEpartmentid = doormath.getRootdepartment(idcenName)
        token = idc.token
        ip = idc.idcIp
        headers = {'Content-Type': 'application/json', 'AccessToken': token}
        if userDepartmentid == rootDEpartmentid or userDepartmentid == False:
            Url = 'https://' + ip + '/api/userGroups'
            html = requests.get(url=Url, data=None, headers=headers, verify=False)
            groupInfo = json.loads(html.text)
            for i in range(len(groupInfo['groups'])):
                groupDict = {}
                groupId = groupInfo['groups'][i]['groupId']
                groupName = groupInfo['groups'][i]['groupName']
                departmentId = groupInfo['groups'][i]['departmentId']
                if departmentId == doormath.getRootdepartment(idcenName)[0]:
                    groupDict['groupId']=groupId
                    groupDict['groupName'] = groupName
                    groupDict['departmentId'] = departmentId
                    grouplist.append(groupDict)
            #print(groupInfo['groups']['groupId'])
            response = {
                "content": grouplist,
                "status":"OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s ,userName : %s ,%s 200 reason:%s" % (request.method,userName ,idcenName, Url,reason))
            return JsonResponse(response, safe=False)
        elif userDepartmentid:
            rulelist = []
            Url = 'https://' + str(ip) + '/api/authorizations/rules'
            html = requests.get(url=Url, data=None, headers=headers, verify=False)
            ruleData = json.loads(html.text)
            # print(len(ruleData['rules']))
            for i in range(len(ruleData['rules'])):
                ruledict = {}
                if ruleData['rules'][i]['ruleName'].startswith('QA'):
                    # print(ruleData['rules'][i]['ruleName'])
                    ruledict['groupName'] = ruleData['rules'][i]['ruleName']
                    ruledict['groupId'] = ruleData['rules'][i]['ruleId']
                    rulelist.append(ruledict)
            response = {
                "content": rulelist,
                "status": "OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s ,userName : %s ,%s 200 reason:%s" % (request.method,idcenName, userName, Url,reason))
            return JsonResponse(response, safe=False)

    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def selectUseridapi(request):
#查询用户id接口
    grouplist=[]
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        Url = 'https://' + ip + '/api/users'
        headers = {'Content-Type': 'application/json', 'AccessToken': token}
        html = requests.get(url=Url, data=None, headers=headers, verify=False)
        userData = json.loads(html.text)
        #print(userData)
        getAlldepartment = doormath.getAlldepartment(idcenName)
        #print(getAlldepartment)
        for i in range(len(userData['users'])):
            #c = '%s,%s,%s,%s,%s' % (userData[i]['username'], userData[i]['userId'], userData[i]['roleName'], userData[i]['departmentId'],userData[i]['nickname'].encode())
            if userData['users'][i]['username'] == userName:
                userdict = {}
                userdict['username'] = userName
                userdict['userId'] = userData['users'][i]['userId']
                userdict['departmentId'] = userData['users'][i]['departmentId']
                for j in range(len(getAlldepartment)):
                    if getAlldepartment[j]['departmentId'] == userData['users'][i]['departmentId']:
                        userdict['departmentName'] = getAlldepartment[j]['departmentName']
                response = {
                "content": userdict,
                "status":"OK",
                "errorMsg": "",
                }
                logger.info(" %s idcenName: %s ,userName : %s ,%s 200 reason:%s" % (request.method,idcenName,userName,Url,reason))
                return JsonResponse(response, safe=False)
        else:
            response = {
                "content": "",
                "status":"ERROR",
                "errorMsg": "用户 %s 不存在" % userName
            }
            logger.error("用户 %s 不存在 404" % userName)
            return JsonResponse(response, safe=False)
    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)


@csrf_exempt
def delUser(request):
#删除用户
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        reason = info.get("reason")
        if userName == 'admin':
            response = {
                "content": '',
                "status": "ERROR",
                "errorMsg": 'can not del admin ',
            }
            logger.error("can not del admin！")
            return JsonResponse(response, safe=False)
        getUserid = doormath.selectUserid(idcenName,userName)
        if getUserid is False:
            response = {
                "content": '',
                "status":"ERROR",
                "errorMsg": 'The username %s is not exsit' % userName,
            }
            logger.error("用户 %s 不存在 404" % userName)
            return JsonResponse(response, safe=False)
        else:
            idc = idcInfo.objects.get(idcName=idcenName)
            token = idc.token
            ip = idc.idcIp
            Url = 'https://' + ip + '/api/users/' + str(getUserid)
            headers = {'Content-Type': 'application/json', 'AccessToken': token}
            html = requests.delete(url=Url, data=None, headers=headers, verify=False)
            response = {
                "content": 'del user %s success' % userName ,
                "status":"OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s ,deluserName : %s ,%s 200 reason:%s" % (request.method,idcenName,userName,Url,reason))
            return JsonResponse(response, safe=False)
    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def selectUserfromgroup(request):
#查询用户信息
#不能查到用户属于哪个用户组，只能查用户组里是否有该用户
    if request.method == 'POST':
        userInfo = {}
        grouplist = []
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        reason = info.get("reason")
        addUserpermission = info.get("permissionList")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        userId = doormath.selectUserid(idcenName,userName)
        userDepartmentid = doormath.selectUserdepartmentid(idcenName,userName)
        selUserpermission = doormath.selectUserpermission(idcenName,userName)
        userInfo['userId'] = userId
        userInfo['userDepartmentid'] = userDepartmentid
        #userInfo['Userpermission'] = selUserpermission
        groupInfo = doormath.selectPermissiongroup(idcenName)[0]
        userPermissionlist=[]
        for i in selUserpermission:
            userPermissiondict={}
            for j in range(len(groupInfo)):
                if groupInfo[j]['groupId'] == i:
                    userPermissiondict['groupId']=i
                    userPermissiondict['groupName'] = groupInfo[j]['groupName']
                    userPermissionlist.append(userPermissiondict)
            userInfo['userPermission'] = userPermissionlist
        if selUserpermission:
            response = {
                "content": userInfo,
                "status": "OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s ,userName %s  is existgroup : %s 200 reason:%s" % (request.method, idcenName, userName,userInfo,reason))
            return JsonResponse(response, safe=False)
        else:
            response = {
                "content": userInfo,
                "status": "ERROR",
                "errorMsg": "user %s is not exist any group" % userName,
            }
            logger.error(" %s idcenName: %s ,userName is not exist any group : %s 404 reason:%s" % (request.method, idcenName, userName,reason))
            return JsonResponse(response,safe=False)
    else:
        response = {
            "content": "",
            "status":"ERROR",
            "errorMsg": "请求参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def resetPassword(request):
#重置密码默认88888888
    if request.method == 'POST':
        passWord =  ''.join(random.sample(string.ascii_letters + string.digits, 8))
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        userId = doormath.selectUserid(idcenName, userName)
        print(userId)
        if userId:
            headers = {'Content-Type': 'application/json', 'AccessToken': token}
            Url = 'https://' + str(ip) + '/api/users/'  + str(userId)
            Data = {"password": passWord }
            webLogininfo = idc.webLogininfo
            sshLogininfo = idc.sshLogininfo
            html = requests.put(url=Url, data=json.dumps(Data), headers=headers, verify=False)
            userData = json.loads(html.text)
            print(userData)
            response = {
                "content": '重置密码完成,密码已邮件发送，若未收到请联系管理员!',
                "status": "OK",
                "errorMsg": "",
            }
            send_mail('堡垒机重置密码', '用户 %s  重置密码为：%s webLogininfo: 请登录 %s 修改密码。\n sshLogininfo: %s' % (userName, passWord, webLogininfo, sshLogininfo),'sa-no-reply@xx.cn', ['liqiao.liu@xxqq.com'],fail_silently=False)
            logger.info(" %s idcenName: %s ,userName %s ,resetPassword %s, 200 reason:%s" % (request.method, idcenName,userName,passWord,reason))
            return JsonResponse(response,safe=False)
        else:
            response = {
                "content": '',
                "status": "ERROR",
                "errorMsg": "参数错误",
            }
            logger.error("请求方法错误 需使用 POST方法！503")
            return JsonResponse(response, safe=False)

@csrf_exempt
def addUsertogroup(request):
#添加新用户到组
    if request.method == 'POST':
        passWord = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        groupIdlist = info.get("permissionList")
        departmentId = info.get("departmentId")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        webLogininfo = idc.webLogininfo
        sshLogininfo = idc.sshLogininfo
        userId = doormath.selectUserid(idcenName,userName)
        if userId:
            response = {
                "content": "用户 %s 已存在" % userName,
                "status": "ERROR",
                "errorMsg": "用户 %s 已存在" % userName,
            }
            logger.error( "%s idcName: %s 添加用户时用户 %s 已存在 400 reason:%s" % (request.method, idcenName,userName,reason))
            return JsonResponse(response,safe=False)
        else:
            addUser = doormath.addUser(idcenName,userName,departmentId,passWord)
            userIdnow = doormath.selectUserid(idcenName,userName)
            userIdnowlist = []
            userIdnowlist.append(userIdnow)
            if addUser:
                for i in groupIdlist:
                    headers = {'Content-Type': 'application/json', 'AccessToken': token}
                    Data =  {"userIds":userIdnowlist}
                    Url = 'https://' + str(ip) + '/api/userGroups/' + str(i) + '/users'
                    html = requests.post(url=Url, data=json.dumps(Data), headers=headers, verify=False)
                    userData = json.loads(html.text)
                response = {
                "content": "添加用户 %s 成功 ! 初始密码已发送邮箱！ webLogininfo: 请登录'%s'修改密码 ,sshLogininfo: '%s'" % (userName,webLogininfo,sshLogininfo),
                "status": "OK",
                "errorMsg": "",
                }
                # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
                #send_mail('堡垒机初始密码', '添加用户 %s 成功 初始密码默认为：%s! webLogininfo: 请登录 %s 修改密码。\n sshLogininfo: %s' % (userName,passWord,webLogininfo,sshLogininfo),'liqiao.liu@xxqq.com',['liqiao.liu@xxqq.com'], fail_silently=False )
                send_mail('堡垒机初始密码', ' 添加用户 %s 成功 初始密码默认为：%s webLogininfo: 请登录 %s 修改密码。\n sshLogininfo: %s' % (userName, passWord, webLogininfo, sshLogininfo),'sa-no-reply@xx.cn', ['liqiao.liu@xxqq.com'],fail_silently=False)
                logger.info("%s idcName: %s 添加用户 %s ，密码: %s,成功 200 reason:%s" % (request.method,idcenName,userName,passWord,reason))
                return JsonResponse(response, safe=False)
                #return JsonResponse({"status:":"ok"}, safe=False)
    else:
        response = {
            "content": '',
            "status": "ERROR",
            "errorMsg": "参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def updateUser(request):
#更新用户信息,比较现有权限和新增权限的差别然后添加权限，目的修改部门和权限组
#修改用户在组的前提是在该用户和用户组都在同一个部门下,考虑不能修改部门，并列出该部门下的所有用户组共用户选择
#判断用户的id是否属于根部门，属于则列出可添加的组（前提：用户组与账户组已有关联的规则），否则就添加用户到已关联用户到账户组的规则中
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        userName = info.get("userName")
        reason = info.get("reason")
        departmentIdlist = info.get("departmentId")
        groupIdlist = info.get("permissionList")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        userId = doormath.selectUserid(idcenName,userName)
        alreadygouplist = sorted(doormath.selectUserpermission(idcenName, userName))
        permissionIdlist = sorted(groupIdlist)
        userDepartmentnow = doormath.selectUserdepartmentid(idcenName,userName)
        rootDepartment = doormath.getRootdepartment(idcenName)[0]
        userIdlist = []
        if userDepartmentnow == rootDepartment:
            #部门为用户根用用户组来操作
            #response = {
            #    "content": "比较部门!部门为根",
            #    "status": "ok",
            #    "errorMsg": "",
            #}
            #return JsonResponse(response, safe=False)
            if userId:
                userIdlist.append(userId)
                alreadyDepartmentid = doormath.selectUserdepartmentid(idcenName,userName)
                #departmentId = departmentIdlist[0]
                #if departmentId == alreadyDepartmentid:
                #    print('部门不变')
                #    pass
                #else:
                    #更新部门
                    #doormath.updateDepartment(idcenName,userName,departmentId)
                #    pass
            if not permissionIdlist:
                #没选择任何权限
                response = {
                    "content": '',
                    "status": "ERROR",
                    "errorMsg": "请选择权限！",
                }
                logger.error("%s idcName: %s userName：%s 没有选择任何权限 400 reason:%s" % (request.method, idcenName, userName,reason))
                return JsonResponse(response, safe=False)
            elif not alreadygouplist:
                #原来权限为空
                for k in permissionIdlist:
                    headers = {'Content-Type': 'application/json', 'AccessToken': token}
                    Data = {"userIds": userIdlist}
                    Url = 'https://' + str(ip) + '/api/userGroups/' + str(k) + '/users'
                    html = requests.post(url=Url, data=json.dumps(Data), headers=headers, verify=False)
                    userData = json.loads(html.text)
                    response = {
                        "content": "更新成功!",
                        "status": "OK",
                        "errorMsg": "",
                    }
                    logger.info(" %s idcenName: %s ,userName : %s ,%s 原有权限为空更新权限成功 200 reason:%s" % (request.method, idcenName, userName, Url,reason))
                    return JsonResponse(response, safe=False)
            elif permissionIdlist and alreadygouplist:
                delPermissionlist = []#删除的权限列表
                addPermissionlist = []#添加的权限列表
                if permissionIdlist == alreadygouplist:
                    response = {
                        "content": '',
                        "status": "OK",
                        "errorMsg": "权限不变！",
                    }
                    logger.info(" %s idcenName: %s ,userName : %s 权限不变 200 reason:%s" % (request.method, idcenName, userName,reason))
                    return JsonResponse(response, safe=False)
                else:
                    for i in alreadygouplist:
                        if i not in permissionIdlist:
                            delPermissionlist.append(i)
                    for m in permissionIdlist:
                        if m not in alreadygouplist:
                            addPermissionlist.append(m)
                    if delPermissionlist:
                        for j in delPermissionlist:
                            headers = {'Content-Type': 'application/json', 'AccessToken': token}
                            Url = 'https://' + str(ip) + '/api/userGroups/' +str(j) + '/users/' + str(userId)
                            html = requests.delete(url=Url, data=None, headers=headers, verify=False)
                        logger.info(" %s idcenName: %s ,userName : %s 删除的权限: %s  200 reason:%s" % (request.method, idcenName, userName,delPermissionlist,reason))
                    if addPermissionlist:
                        for n in addPermissionlist:
                            headers = {'Content-Type': 'application/json', 'AccessToken': token}
                            Data = {"userIds": userIdlist}
                            Url = 'https://' + str(ip) + '/api/userGroups/' +str(n) + '/users'
                            html = requests.post(url=Url, data=json.dumps(Data), headers=headers, verify=False)
                            userData = json.loads(html.text)
                        logger.info(" %s idcenName: %s ,userName : %s 添加的权限: %s  200 reason:%s" % (request.method, idcenName, userName, addPermissionlist,reason))
                response = {
                    "content": "更新成功!",
                    "status": "OK",
                    "errorMsg": "",
                }
                logger.info(" %s idcenName: %s ,userName : %s 添加和删除的权限: %s %s  200 reason:%s" % (request.method, idcenName, userName, addPermissionlist,delPermissionlist,reason))
                return JsonResponse(response, safe=False)
        elif userDepartmentnow:
            #部门不是根老用户把用户添加到指定的规则名称中，并事先绑定好账户组
            ruleIdlist = info.get("groupIdlist")
            m = doormath.addPermission(idcenName,userName,ruleIdlist)
            if m:
                response = {
                    "content": "老用户添加规则成功!",
                    "status": "OK",
                    "errorMsg": "",
                }
                logger.info(" %s idcenName: %s ,userName : %s 添加规则: %s  200 reason:%s" % (request.method, idcenName, userName, ruleIdlist,reason))
                return JsonResponse(response, safe=False)
            else:
                response = {
                    "content": '',
                    "status": "ERROR",
                    "errorMsg": "参数错误",
                }
                logger.error("请求方法错误！503")
                return JsonResponse(response, safe=False)
    else:
        response = {
            "content": '',
            "status": "ERROR",
            "errorMsg": "参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def getRule(request):
#得到授权规则并展现规则名给不在用户根部门的老用户
    if request.method == 'POST':
        rulelist= []
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        reason = info.get("reason")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        headers = {'Content-Type': 'application/json', 'AccessToken': token}
        Url = 'https://' + str(ip) + '/api/authorizations/rules'
        html = requests.get(url=Url, data=None, headers=headers, verify=False)
        ruleData = json.loads(html.text)
        #print(len(ruleData['rules']))
        for i in range(len(ruleData['rules'])):
            ruledict = {}
            if ruleData['rules'][i]['ruleName'].startswith('QA'):
                #print(ruleData['rules'][i]['ruleName'])
                ruledict['groupName'] = ruleData['rules'][i]['ruleName']
                ruledict['groupId'] = ruleData['rules'][i]['ruleId']
                rulelist.append(ruledict)
        response = {
            "content": rulelist,
            "status": "OK",
            "errorMsg": "",
        }
        logger.info(" %s idcenName: %s getrules 200 reason:%s " % (request.method, idcenName,reason))
        return JsonResponse(response, safe=False)
    else:
        response = {
            "content": '',
            "status": "ERROR",
            "errorMsg": "参数错误",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

def addPermission(request):
#对部门不是根的老用户添加规则
    info = json.loads(request.body.decode())
    idcenName = info.get("idcName")
    userName = info.get("userName")
    ruleIdlist = info.get("permissionList")
    reason = info.get("reason")
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    userId = doormath.selectUserid(idcenName,userName)
    userIdlist = []
    userIdlist.append(userIdlist)
    data={'userAttachIds':userIdlist}
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    if ruleIdlist:
        for ruleId in ruleIdlist:
            Url= 'https://' + str(ip) + '/api/authorizations/rules/'+ str(ruleId)
            html = requests.put(url=Url, data=None, headers=headers, verify=False)
            ruleData = json.loads(html.text)
            response = {
                "content": '添加规则成功！',
                "status": "OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s ,userName : %s 添加规则: %s , %s 200,reason:%s" % (request.method, idcenName, userName, ruleIdlist,Url,reason))
            return JsonResponse(response, safe=False)
    else:
        response = {
            "content": '',
            "status": "ERROR",
            "errorMsg": "参数错误！",
        }
        logger.error("请求方法错误 需使用 POST方法！503")
        return JsonResponse(response, safe=False)

@csrf_exempt
def addTmppermission(request):
#添加临时规则
    pass

@csrf_exempt
def addHost(request):
#添加主机并添加主机账户默认(sysops,loguser)
    if request.method == 'POST':
        info = json.loads(request.body.decode())
        idcenName = info.get("idcName")
        idc = idcInfo.objects.get(idcName=idcenName)
        token = idc.token
        ip = idc.idcIp
        hostIp = info.get("hostIp")
        accountList = info.get("account")
        authMode = info.get('authMode')
        protocol = info.get('protocol')
        try:
            IPy.IP(hostIp)
        except:
            response = {
                "content": "",
                "status": "ERROR",
                "errorMsg": "hostip %s is error !" % hostIp,
            }
            logger.info(" %s idcenName: %s add host %s  ip error 503 " % (request.method, idcenName, hostIp))
            return JsonResponse(response, safe=False)
        hostNamelist = hostIp
        getRootdepartmentId = doormath.getRootdepartment(idcenName)[0]
        hostId = doormath.Retrieve_host(idcenName,hostIp)
        if hostId:
            response = {
                "content": "",
                "status": "ERROR",
                "errorMsg": "hostip %s already exist !" % hostIp,
            }
            logger.info(" %s idcenName: %s add host %s  already exist 503 " % (request.method, idcenName, hostIp))
            return JsonResponse(response, safe=False)
        Url = 'https://' + str(ip) + '/api/hosts'
        headers = {'Content-Type': 'application/json', 'AccessToken': token}
        data={'departmentId':getRootdepartmentId,'hostIp':hostIp,'hostname':hostIp}
        print(data,Url)
        html = requests.post(url=Url, data=json.dumps(data), headers=headers, verify=False)
        getHostid = doormath.Retrieve_host(idcenName,hostIp)
        print(getHostid)
        if int(getHostid):
            if authMode == "manualLogin" and protocol == 'FTP':
                account=None
                password=None
                doormath.addHostaccount(idcenName,getHostid,account,password,authMode,protocol)
            elif authMode == "manualLogin" and protocol == 'RDP':
                account = None
                password = None
                doormath.addHostaccount(idcenName,getHostid,account,password,authMode,protocol)
            else:
                for account,password in accountList.items():
                    doormath.addHostaccount(idcenName,getHostid,account,password)
            response = {
                "content": "",
                "status": "OK",
                "errorMsg": "",
            }
            logger.info(" %s idcenName: %s add host %s 200 " % (request.method, idcenName,hostIp))
            return JsonResponse(response, safe=False)
        else:
            response = {
                "content": "",
                "status": "ERROR",
                "errorMsg": "参数错误！",
            }
            logger.info(" %s idcenName: %s add host %s 503 " % (request.method, idcenName, hostIp))
            return JsonResponse(response, safe=False)

@csrf_exempt
def addHosttohostgroup(request):
#添加主机到组
    pass



