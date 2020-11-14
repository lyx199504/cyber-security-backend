#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/12 21:44
# @Author : LYX-夜光

import json
import requests

from cyber_security.conf.configReader import ConfigReader

# 请求url
def requestUrl(url, mothed="GET", data={}):
    try:
        if mothed == "GET":
            response = requests.get(url=url)
        else:
            data = json.dumps(data)
            response = requests.post(url=url, data=data)
        content = response.content
        return json.loads(content)
    except:
        return {}

# 获取微信用户信息
def requestWechat(code):
    appid = ConfigReader.getStrConfig("wechat", "appid")
    secret = ConfigReader.getStrConfig("wechat", "appSecret")
    # 小程序开发文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
    # 根据appid,secret和前端发送的code，获取openid
    url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (appid, secret, code)
    response = requestUrl(url)
    openId = response.get('openid', "")
    return openId

if __name__ == "__main__":
    print(requestWechat("111"))