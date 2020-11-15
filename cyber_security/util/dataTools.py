#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/5 9:19
# @Author : LYX-夜光
import json

from django.core.serializers.json import DjangoJSONEncoder
from django_redis import get_redis_connection

class RedisData:
    prefix = "cyber_security"
    DATA_TIME = 60*60*24*30  # 30天
    redisConn = get_redis_connection()

    @staticmethod  # 数据库数据key
    def getDataKey(model, id):
        return '/%s/%s/%s' % (RedisData.prefix, model, id)

    @staticmethod  # 用户sn key
    def getSnKey(userId):
        return '/%s/user/%s/sn' % (RedisData.prefix, userId)

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

    @staticmethod  # 在redis中获取批量数据
    def getDataList(keyList):
        try:
            redisConn = RedisData.redisConn.pipeline(transaction=False)
            for key in keyList:
                redisConn.get(key)
            results = redisConn.execute()
            return results
        except:
            return [None]*len(keyList)

    @staticmethod  # 在redis中批量设置信息， keyValue键值对， time设置时间（单位：s）
    def setDataList(keyValue, time=-1, dumps=True):
        try:
            redisConn = RedisData.redisConn.pipeline(transaction=False)
            for key in keyValue:
                if dumps:
                    redisConn.set(key, json.dumps(keyValue[key], cls=DjangoJSONEncoder))
                else:
                    redisConn.set(key, keyValue[key])
                if time > -1:
                    redisConn.expire(key, time)
            redisConn.execute()
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
        return model.objects.create(**data)

    @staticmethod  # 先在redis后在db中获取多个数据
    def getDataList(model, idList):
        modelName = model._meta.object_name
        modelName = modelName[0].lower() + modelName[1:]
        keyList = list(map(lambda x: RedisData.getDataKey(modelName, x), idList))
        dataList = RedisData.getDataList(keyList)
        # 判断redis中有没有数据
        unsolvedIdIndex, unsolvedIdList = [], []
        for i in range(len(idList)):
            if dataList[i]:
                dataList[i] = json.loads(dataList[i])
            else:
                unsolvedIdIndex.append(i)
                unsolvedIdList.append(idList[i])
        if unsolvedIdList:  # 若redis没有，则查询mysql
            tableName = model._meta.db_table
            conditionList = ['WHEN ' + tableName+'_id' + '=%s THEN %s' % (pk, index) for index, pk in enumerate(unsolvedIdList)]
            ordering = "CASE %s END" % ' '.join(conditionList)  # 使得查表时不改变顺序
            datas = list(model.objects.filter(**{modelName+'Id__in': unsolvedIdList}).values(*model.allowFields()).extra(select={'ordering': ordering}, order_by=('ordering',)))
            keyList = list(map(lambda x: RedisData.getDataKey(modelName, x), unsolvedIdList))
            keyValue = dict(zip(keyList, datas))
            RedisData.setDataList(keyValue, RedisData.DATA_TIME)
            for i in range(len(unsolvedIdList)):
                dataList[unsolvedIdIndex[i]] = datas[i]
        return dataList