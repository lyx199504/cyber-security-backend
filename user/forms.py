#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/13 13:47
# @Author : LYX-夜光
from django import forms

from cyber_security.util.viewsTools import NewForm


# 用户登录表单
class UserLoginForm(NewForm):
    nickname = forms.CharField(error_messages={'required': '昵称不能为空'})
    image = forms.CharField(error_messages={'required': '图片不能为空'})
    gender = forms.IntegerField(error_messages={'required': '性别不能为空', 'invalid': '性别填写错误!'}, min_value=0, max_value=2)
    code = forms.CharField(error_messages={'required': 'code不能为空'})

# 用户排名表单
class UserRankForm(NewForm):
    offset = forms.IntegerField(required=False, error_messages={'invalid': '填数字！不然就不要填！'}, min_value=0)
    limit = forms.IntegerField(required=False, error_messages={'invalid': '填数字！不然就不要填！'}, min_value=1, max_value=10)