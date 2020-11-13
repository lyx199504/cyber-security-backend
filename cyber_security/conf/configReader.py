#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2018/9/11 14:47
# @Author : snowmusic

import os
import configparser
import codecs

class ConfigReader:
    configPath = os.path.join(os.path.dirname(__file__), "config.conf")
    appConfig = configparser.ConfigParser()
    with codecs.open(configPath, 'r', encoding='utf-8') as config:
        appConfig.read_file(config)

    @staticmethod
    def getStrConfig(section, option):
        return str(ConfigReader.appConfig.get(section, option))

    @staticmethod
    def getIntConfig(section, option):
        return int(ConfigReader.appConfig.get(section, option))

    @staticmethod
    def getUnicodeConfig(section, option):
        return ConfigReader.appConfig.get(section, option)
