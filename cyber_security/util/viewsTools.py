#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/2 15:03
# @Author : LYX-夜光

from django import forms
from django.http.multipartparser import MultiPartParser
from django.views import View

from cyber_security.util.tokenTools import Token


class NewView(View):
    def setHeaders(self):
        self.sn = self.request.META.get('HTTP_SN', "")

    def getPost(self):
        return self.request.POST.dict()

    def getPut(self):
        return MultiPartParser(self.request.META, self.request, self.request.upload_handlers).parse()[0].dict()

    # 用户认证
    def userAuth(self):
        self.setHeaders()
        self.userId = Token.validSn(self.sn)
        if not self.userId:
            raise Exception('userAuthException')

# 表单
class NewForm(forms.Form):
    def errorsDict(self):
        errorDict = dict(self.errors)
        return {key: errorDict[key][0] for key in errorDict}