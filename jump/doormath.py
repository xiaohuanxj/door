#!/usr/bin/env python
# coding=utf-8
# description            :
# author                 : 'simle'
# version                :0.1
# usage                  :python 
# packages               :
# python_version         :2.7.13
# @Time                  : 2018/8/2
# @Site                  : 
# @File                  : math.py
# @Software              : PyCharm
import json,requests,sys

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
#from pip._vendor import requests
from jump.models import idcInfo

@csrf_exempt
def selectUserid(idcenName,userName):
#查询用户id信息
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + ip + '/api/users'
    #print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.get(url=Url, data=None, headers=headers, verify=False)
    userData = json.loads(html.text)
    #print(userData)
    for i in range(len(userData['users'])):
        #c = '%s,%s,%s,%s,%s' % (userData[i]['username'], userData[i]['userId'], userData[i]['roleName'], userData[i]['departmentId'],userData[i]['nickname'].encode())
        if userData['users'][i]['username'] == userName:
            userdict = {}
            userdict['username'] = userName
            userdict['userId'] = userData['users'][i]['userId']
            userdict['departmentId'] = userData['users'][i]['departmentId']
            return userData['users'][i]['userId']
    else:
        return False

@csrf_exempt
def selectUserdepartmentid(idcenName,userName):
#查询用户部门id信息
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + ip + '/api/users'
    #print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.get(url=Url, data=None, headers=headers, verify=False)
    userData = json.loads(html.text)
    #print(userData)
    for i in range(len(userData['users'])):
        #c = '%s,%s,%s,%s,%s' % (userData[i]['username'], userData[i]['userId'], userData[i]['roleName'], userData[i]['departmentId'],userData[i]['nickname'].encode())
        if userData['users'][i]['username'] == userName:
            userdict = {}
            userdict['username'] = userName
            userdict['userId'] = userData['users'][i]['userId']
            userdict['departmentId'] = userData['users'][i]['departmentId']
            return userData['users'][i]['departmentId']
    else:
        return False

@csrf_exempt
def selectPermissiongroup(idcenName):
#查询权限组信息
    groupInfolist = []
    grouplist = []
    groupIdlist = []
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + ip + '/api/userGroups'
    #print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.get(url=Url, data=None, headers=headers, verify=False)
    groupInfo = json.loads(html.text)
    #print(groupInfo['groups'])
    for i in range(len(groupInfo['groups'])):
        groupDict = {}
        groupId = groupInfo['groups'][i]['groupId']
        groupName = groupInfo['groups'][i]['groupName']
        departmentId = groupInfo['groups'][i]['departmentId']
        groupDict['groupId']=groupId
        groupDict['groupName'] = groupName
        groupDict['departmentId'] = departmentId
        grouplist.append(groupDict)
    #print(groupInfo['groups']['groupId'])
        groupIdlist.append(groupDict)
        groupInfolist.append(groupId)
    #print(groupIdlist)
    return groupIdlist,groupInfolist

@csrf_exempt
def selectUserpermission(idcenName,userName):
# 查询用户已有权限
    userGroupidlist=[]
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    getUserid = selectUserid(idcenName,userName)
    if getUserid is False:
        return "user %s is not exist" % userName
    getGrouplist = selectPermissiongroup(idcenName)[1]
    #print(getGrouplist)
    #print(getGroupid)
    #print(getUserid)
    Url='https://' + ip  + '/api/userGroups/'
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    #print(getGroupid)
    for i in range(len(getGrouplist)):
        #print(getGrouplist[i])
        endUrl = Url  +  str(getGrouplist[i]) + '/users/' + str(getUserid)
        #print(endUrl)
        #print(getGrouplist[i])
        html = requests.get(url=endUrl , data=None, headers=headers, verify=False)
        userData = json.loads(html.text)
        #print(userData)
        if 'username' in userData.keys():
            #print(getGroupid[i])
            userGroupidlist.append(getGrouplist[i])
            #print(userGroupidlist)
    return userGroupidlist

@csrf_exempt
def addUser(idcenName,userName,departmentId,passWord,roleName='operator'):
# 添加用户默认权限运维员operator，默认密码88888888
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Data = {"departmentId": departmentId , "nickname": userName ,"username": userName ,"roleName": roleName ,"password": passWord }
    Url='https://' + ip  + '/api/users'
    print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.post(url=Url , data=json.dumps(Data), headers=headers, verify=False)
    userData = json.loads(html.text)
    print(userData)
    return 1

@csrf_exempt
def updateDepartment(idcenName,userName,departmentId):
# 不能修改部门
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Data = {"departmentId": departmentId}
    userId = selectUserid(idcenName,userName)
    Url='https://' + ip  + '/api/users/' + str(userId)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.put(url=Url , data=json.dumps(Data), headers=headers, verify=False)
    #userData = json.loads(html.text)
    #return 1

@csrf_exempt
def getRootdepartment(idcenName):
#查询部门信息
    departMentlist = []
    departMentrootlist = []
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + ip + '/api/departments'
    #print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html=requests.get(url=Url, data=None,headers=headers,verify=False)
    departMentinfo=json.loads(html.text)
    for i in range(len(departMentinfo['departments'])):
        departMentdict = {}
        departmentid = departMentinfo['departments'][i]['departmentId']
        departmentname = departMentinfo['departments'][i]['departmentName']
        if departMentinfo['departments'][i]['departmentName']== '用户根':
            departMentdict['departmentId'] = departmentid
            departMentdict['departmentName'] = departmentname
        #print(departmentid,departmentname)
        return departmentid,departmentname

@csrf_exempt
def getAlldepartment(idcenName):
#查询部门信息
    departMentlist = []
    departMentrootlist = []
    idc = idcInfo.objects.get(idcName=idcenName)
    print(idc)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + ip + '/api/departments'
    #print(Url)
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html=requests.get(url=Url, data=None,headers=headers,verify=False)
    departMentinfo=json.loads(html.text)
    for i in range(len(departMentinfo['departments'])):
        departMentdict = {}
        departmentid = departMentinfo['departments'][i]['departmentId']
        departmentname = departMentinfo['departments'][i]['departmentName']
        departMentdict['departmentId'] = departmentid
        departMentdict['departmentName'] = departmentname
        #print(departmentid,departmentname)
        departMentlist.append(departMentdict)
    print(departMentlist)
    return departMentlist

@csrf_exempt
def addPermission(idcenName,userName,ruleIdlist):
#对部门不是根的老用户添加规则
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    userId = selectUserid(idcenName,userName)
    userIdlist = []
    userIdlist.append(userId)
    Data={'userAttachIds':userIdlist}
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    if ruleIdlist:
        for ruleId in ruleIdlist:
            Url= 'https://' + str(ip) + '/api/authorizations/rules/'+ str(ruleIdlist[0])
            print(Url)
            html = requests.put(url=Url, data=json.dumps(Data), headers=headers, verify=False)
            ruleData = json.loads(html.text)
            print(ruleData)
        return 1
    else:
        return False

@csrf_exempt
def addTmppermission(idcenName,userName,ruleIdlist):
#对部门不是根的老用户添加规则
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    userId = selectUserid(idcenName,userName)
    userIdlist = []
    userIdlist.append(userId)
    Data={'userAttachIds':userIdlist}
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    if ruleIdlist:
        for ruleId in ruleIdlist:
            Url= 'https://' + str(ip) + '/api/authorizations/rules/'+ str(ruleIdlist[0])
            print(Url)
            html = requests.put(url=Url, data=json.dumps(Data), headers=headers, verify=False)
            ruleData = json.loads(html.text)
            print(ruleData)
        return 1
    else:
        return False




#############
#主机操作

@csrf_exempt
def Retrieve_host(idcenName,hostIp):
    #查询主机hostID
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + str(ip) + '/api/hosts'
    data = None
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.get(url=Url, data=None, headers=headers, verify=False)
    host_list = json.loads(html.text)['hosts']
    for i in range(len(host_list)):
        if hostIp.strip()==host_list[i]['hostIp']:
            print(host_list[i]['hostId'])
            return host_list[i]['hostId']
    else:
        return False

@csrf_exempt
def addHostaccount(idcenName,hostId,accountName,passWord,authMode='autoLogin',protocol='SSH'):
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + str(ip) + '/api/hosts/' + str(hostId) + '/accounts'
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    if authMode == "autoLogin":
        data={'accountName':accountName,'password':passWord,'authMode':authMode,'protocol':protocol}
        html = requests.post(url=Url, data=json.dumps(data), headers=headers, verify=False)
        print(html.text)
    else:
        data = {'authMode': authMode, 'protocol': protocol}
        html = requests.post(url=Url, data=json.dumps(data), headers=headers, verify=False)
        print(html.text)


@csrf_exempt
def Get_hostgroupid(idcenName,hostgroup_name):
    #得到所有主机组id
    data=None
    idc = idcInfo.objects.get(idcName=idcenName)
    token = idc.token
    ip = idc.idcIp
    Url = 'https://' + str(ip) + '/api/hostGroups'
    headers = {'Content-Type': 'application/json', 'AccessToken': token}
    html = requests.get(url=Url, data=json.dumps(data), headers=headers, verify=False)
    hostgroup_data = json.loads(html.text)['groups']
    print(hostgroup_data)
    for i in range(len(hostgroup_data)):
        c = '%s,%s,%s' % (hostgroup_data[i]['groupId'], hostgroup_data[i]['departmentId'], hostgroup_data[i]['groupName'])
        #print c
        if hostgroup_data[i]['departmentId']== getRootdepartment(idcenName):
            #print hostgroup_data[i]['groupId']
            return hostgroup_data[i]['groupId'],hostgroup_data[i]['groupName']

@csrf_exempt
def Add_host_to_hostgroup(idcenName,hostgroupname,hostip):
    #把主机添加到主机组
    pass
    #idc = idcInfo.objects.get(idcName=idcenName)
    #token = idc.token
    #ip = idc.idcIp
    #hostgroupid = Get_hostgroupid(hostgroupname)
    #Url = self.HostGroup_api + '/' + str(hostgroupid) + '/hosts'
    #HostID_list = []
    #HostID_list.append(self.Retrieve_host(hostip))
    #data = {'hostIds': HostID_list}
    #print(data,Url)
    #req = requests.post(Url, json.dumps(data), self.Header)