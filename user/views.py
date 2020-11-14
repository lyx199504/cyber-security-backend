import datetime

from django.shortcuts import render

# Create your views here.
from cyber_security.util.httpTools import RestResponse
from cyber_security.util.tokenTools import Token
from cyber_security.util.viewsTools import NewView
from user import wechatAuth

from user.forms import UserLoginForm
from user.models import User

# 用户登录
class UserLoginView(NewView):
    def post(self, request):
        form = UserLoginForm(self.getPost())
        if not form.is_valid():
            return RestResponse.frontFail("登录失败！", form.errorsDict())
        data = form.cleaned_data
        openId = wechatAuth.requestWechat(data["code"])
        if not openId:
            return RestResponse.userFail("登录失败！")
        data['openId'] = openId
        data['loginTime'] = datetime.datetime.now()
        del data['code']
        user = User.objects.filter(openId=openId).values('userId').first()
        if user:
            userId = user['userId']
        else:
            user = User.objects.create(**data)
            userId = user.userId
        sn = Token.setSn(userId)
        return RestResponse.success("登录成功！", {"userId": userId, "sn": sn})