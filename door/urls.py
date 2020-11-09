#!/usr/bin/env python
# coding=utf-8
"""door URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from jump import views


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^jump/v1/queryidc$', views.queryIdc),
    url(r'^jump/v1/apitype$', views.apiType),
    url(r'^jump/v1/department$', views.getDepartment),
    url(r'^jump/v1/usergroup$', views.permissionGroup),
    url(r'^jump/v1/verifyuser$', views.selectUseridapi),
    url(r'^jump/v1/userpermission$', views.selectUserfromgroup),
    url(r'^jump/v1/userid$', views.selectUseridapi),
    url(r'^jump/v1/getrule$', views.getRule),
    url(r'^jump/v1/resetpwd$', views.resetPassword),
    url(r'^jump/v1/updateuser$', views.updateUser),
    url(r'^jump/v1/tmppermission$', views.addTmppermission),
    url(r'^jump/v1/adduser$', views.addUsertogroup),
    url(r'^jump/v1/deluser$', views.delUser),
    url(r'^jump/v1/addhost$', views.addHost),
    url(r'^jump/v1/addhosttogroup$', views.addHosttohostgroup),

    #url(r'^*$', views.error),
]
