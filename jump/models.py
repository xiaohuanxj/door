#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User



class idcInfo(models.Model):
    id = models.AutoField(primary_key=True, db_column='id', default=1)
    idcIp = models.CharField(max_length=32, verbose_name=u'机房IP',unique=True)
    token = models.CharField(max_length=128, verbose_name=u'token',unique=True)
    zhName = models.CharField(max_length=32, verbose_name=u'机房中文名称',unique=True)
    idcName = models.CharField(max_length=16, verbose_name=u'机房英文名称',unique=True)
    webLogininfo = models.CharField(max_length=128,verbose_name=u'web登陆地址',unique=True)
    sshLogininfo = models.CharField(max_length=128,verbose_name=u'ssh登陆地址',unique=True)
    detail = models.TextField(max_length=256,verbose_name=u'描述')
    #def __unicode__(self):
        #return self.Meta


'''class invokOrbit(models.Model):
    id = models.AutoField(primary_key=True, db_column='id', default=1)
    idcId = models.CharField(max_length=32, verbose_name=u'机房ID', unique=True)
    userId = models.CharField(max_length=32, verbose_name=u'工号', unique=True)
    url = models.CharField(max_length=128, verbose_name=u'调用的url', unique=True)
    params = models.CharField(max_length=128, verbose_name=u'参数json类型',default='', unique=True)
    status = models.CharField(max_length=128, verbose_name=u'状态 bool', unique=True)
    returnInfo = models.CharField(max_length=128, verbose_name=u'返回信息', unique=True)
    requestTime = models.DateField(max_length=128, verbose_name=u'请求时间', auto_now = True)
    def __unicode__(self):
        return self.Meta

class departMent(models.Model):
    id = models.AutoField(primary_key=True, db_column='id', default=1)
    idcId = models.CharField(max_length=32, verbose_name=u'机房IP', unique=True)
    departmentId = models.CharField(max_length=16, verbose_name=u'部门ID', unique=True)
    zhName = models.CharField(max_length=128, verbose_name=u'部门中文名称', unique=True)
    enName = models.CharField(max_length=64, verbose_name=u'部门英文名称', unique=True)
    def __unicode__(self):
        return self.Meta'''


