import datetime

from django.shortcuts import render

# Create your views here.
from cyber_security.util.dataTools import Data
from cyber_security.util.httpTools import RestResponse
from cyber_security.util.tokenTools import Token
from cyber_security.util.viewsTools import NewView
from user import wechatAuth

from user.forms import UserLoginForm
from user.models import User, Checkin


# 用户登录
class UserLoginView(NewView):
    def post(self, request):
        form = UserLoginForm(self.POST())
        if not form.is_valid():
            return RestResponse.frontFail("参数错误！", form.errorsDict())
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
            user = Data.createData(User, data)
            userId = user.userId
        sn = Token.setSn(userId)
        return RestResponse.success("登录成功！", {"userId": userId, "sn": sn})

# 用户信息
class UserSelfView(NewView):
    def get(self, request):
        self.userAuth()
        data = Data.getData(User, self.userId)
        return RestResponse.success("获取自己的信息成功！", data)

# 用户签到
class UserCheckinView(NewView):
    def post(self, request):
        self.userAuth()
        checkinScore = 5  # 签到奖励积分
        try:
            Data.createData(Checkin, {"userId": self.userId})
            data = Data.getData(User, self.userId)
            user = {"userId": self.userId, "score": data['score'] + checkinScore}
            Data.updateData(User, user)
            return RestResponse.success("签到成功！", {"score": checkinScore})
        except:
            return RestResponse.userFail("你今天已签到，不能重复签到哟!")
