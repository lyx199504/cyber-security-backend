#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/14 21:26
# @Author : LYX-夜光
from django import forms
from django.core.validators import RegexValidator

from cyber_security.util.viewsTools import NewForm


# 获取题目表单
class QuestionForm(NewForm):
    type = forms.IntegerField(error_messages={'required': '题型不能为空', 'invalid': '填写整数!'}, min_value=1, max_value=3)
    questionNum = forms.IntegerField(required=False, error_messages={'invalid': '填写整数!'}, min_value=1, max_value=10)

# 答题判断表单
class QuestionByIdForm(NewForm):
    answerList = forms.CharField(required=False, validators=[RegexValidator(r'^\[(\d+(,\d+)*)*\]$', '以列表格式填写！')])