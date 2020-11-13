#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/13 13:47
# @Author : LYX-夜光
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from cyber_security.util.viewsTools import NewForm


# 用户登录表单
class UserLoginForm(NewForm):
    nickname = forms.CharField(error_messages={'required': '昵称不能为空'})
    image = forms.CharField(error_messages={'required': '图片不能为空'})
    gender = forms.IntegerField(error_messages={'required': '性别不能为空', 'invalid': '性别填写错误!', },
                                validators=[MinValueValidator(0, '性别填写错误!'), MaxValueValidator(2, '性别填写错误!')])
    code = forms.CharField(error_messages={'required': 'code不能为空'})