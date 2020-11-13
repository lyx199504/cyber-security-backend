#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/5 9:19
# @Author : LYX-夜光
import json

from django.core.serializers.json import DjangoJSONEncoder
from django_redis import get_redis_connection

class RedisData:
    DATA_TIME = 60*60*24*30  # 30天
    redisConn = get_redis_connection()

    @staticmethod  # 数据库数据key
    def getDataKey(model, id):
        return '/%s/%s' % (model, id)

    @staticmethod  # 用户sn key
    def getSnKey(userId):
        return '/user/%s/sn' % userId

    @staticmethod  # 在redis中获取单个数据
    def getData(key, loads=True):
        try:
            results = RedisData.redisConn.get(key)
        except:
            results = {}
        return results if not results or not loads else json.loads(results)

    @staticmethod  # 在redis中设置信息， key键， results值， time设置时间（单位：s）
    def setData(key, results, time=-1, dumps=True):
        try:
            if dumps:
                RedisData.redisConn.set(key, json.dumps(results, cls=DjangoJSONEncoder))
            else:
                RedisData.redisConn.set(key, results)
            if time > -1:
                RedisData.redisConn.expire(key, time)
            return True
        except:
            return False


class Data:
    @staticmethod  # 先在redis后在db中获取数据
    def getData(model, id):
        modelName = model._meta.object_name
        modelName = modelName[0].lower() + modelName[1:]
        key = RedisData.getDataKey(modelName, id)
        data = RedisData.getData(key)
        if not data:
            data = model.objects.filter(**{modelName+'Id': id}).values(*model.allowFields()).first()
            if data:
                RedisData.setData(key, data, RedisData.DATA_TIME)
            else:
                data = {}
        return data

    @staticmethod  # 先在db后在redis中更新数据
    def updateData(model, data):
        modelName = model._meta.object_name
        modelName = modelName[0].lower() + modelName[1:]
        modelId = modelName+'Id'
        success = model.objects.filter(**{modelId: data[modelId]}).update(**data)
        if success:
            data = model.objects.filter(**{modelId: data[modelId]}).values(*model.allowFields()).first()
            if data:
                key = RedisData.getDataKey(modelName, data[modelId])
                RedisData.setData(key, data, RedisData.DATA_TIME)
        return success

    @staticmethod
    def createData(model, data):
        try:
            return model.objects.create(**data)
        except:
            return False