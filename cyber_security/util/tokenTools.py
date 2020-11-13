#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/11/5 11:12
# @Author : LYX-夜光

import time
import random
import hashlib
import base64

from cyber_security.util.dataTools import RedisData


class Token:
    REDIS_TIME = 60*60*24*7  # 7天

    # DBJ2 Hash算法
    def DBJHash(self, strValue):
        hashValue = 6359  # 稍微大的素数即可，比如：5381
        for char in strValue:
            hashValue = (((hashValue << 5) + hashValue) + ord(char)) & 0xffffffff
        return hashValue

    # token认证，生成sn
    def encodeSn(self, id):
        prefixCode = self.DBJHash("user")  # 前缀码
        originStr = "user" + str(time.time()) + str(random.random())  # 原始串
        originHash = hashlib.md5(originStr.encode('utf-8')).hexdigest()[16:]  # 哈希串
        idCode = (self.DBJHash(originHash) | prefixCode) ^ id  # id编码加密，异或是为了可以在解密时通过id编码拿到id
        pieceStr = originHash + "_" + str(idCode)  # 哈希串和id编码拼接
        pieceStrMap = str(((self.DBJHash(pieceStr) ^ 5381) & 0xffff) % 10000)  # 映射
        linkStr = pieceStr + "/" + pieceStrMap
        return base64.b64encode(linkStr.encode('utf-8')).decode()  # base64编码为sn

    # 解码sn，获取id，encodeSn的逆算法
    def decodeSn(self, sn):
        try:
            prefixCode = self.DBJHash("user")
            pieceStrList = base64.b64decode(sn.encode('utf-8')).decode().split("/")
            if len(pieceStrList) != 2:
                return None
            pieceStr, pieceStrMap = pieceStrList
            if pieceStrMap != str(((self.DBJHash(pieceStr) ^ 5381) & 0xffff) % 10000):
                return None
            splitList = pieceStr.split("_")
            if len(splitList) != 2:
                return None
            originHash, idCode = splitList
            id = (self.DBJHash(originHash) | prefixCode) ^ int(idCode)
            return id
        except:
            return None

    # 根据id在redis中获取sn
    def getSn(self, id):
        key = RedisData.getSnKey(id)
        return RedisData.getData(key)

    @staticmethod  # 验证sn
    def validSn(sn):
        token = Token()
        id = token.decodeSn(sn)
        if id:
            sn_redis = token.getSn(id)
            if sn_redis == sn:
                return id
        return None

    @staticmethod  # 将sn与id分别存入redis
    def setSn(id):
        token = Token()
        key = RedisData.getSnKey(id)
        sn = token.encodeSn(id)
        success = RedisData.setData(key, sn, Token.REDIS_TIME)
        return sn if success else ""
