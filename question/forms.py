#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/14 21:26
# @Author : LYX-夜光
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from cyber_security.util.viewsTools import NewForm


# 获取题目表单
class QuestionForm(NewForm):
    type = forms.IntegerField(error_messages={'required': '题型不能为空', 'invalid': '题型填写错误!'},
                              validators=[MinValueValidator(1, '题型填写错误!'), MaxValueValidator(3, '题型填写错误!')])