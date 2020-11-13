import datetime
import os

import django
from django.test import TestCase

# Create your tests here.

os.environ['DJANGO_SETTINGS_MODULE'] = 'cyber_security.settings'
django.setup()

from cyber_security.util.dataTools import Data
from question.models import Question, Option

# 题目数据库
if __name__ == "__main__":
    with open("content.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        line = lines[i].strip().split()
        if line[0] == '+' or line[0] == '-':
            now = datetime.datetime.now()
            data = {}
            data['createTime'] = data['updateTime'] = now
            if line[0] == '+':  # 判断题
                data['type'] = 1
                data['isCorrect'] = int(line[-1])
                data['content'] = "".join(line[1:-1])
                q = Question.objects.filter(**{'content': data['content'], 'type': data['type']}).values('questionId').first()
                if q:
                    continue
                Data.createData(Question, data)
            else:  # 选择题
                data['isCorrect'] = 0
                data['content'] = "".join(line[1:])
                correct = 0
                options = []
                while i < len(lines)-1:
                    line = lines[i+1].strip().split()
                    option = {}
                    if line[0] != '+' and line[0] != '-':
                        option['content'] = "".join(line[1:-1])
                        option['isCorrect'] = int(line[-1])
                        correct += int(line[-1])
                        option['createTime'] = option['updateTime'] = now
                        options.append(option)
                    else:
                        break
                    i += 1
                if correct <= 1:
                    data['type'] = 2
                else:
                    data['type'] = 3
                q = Question.objects.filter(**{'content': data['content'], 'type': data['type']}).values('questionId').first()
                if q:
                    continue
                question = Data.createData(Question, data)
                for option in options:
                    option['questionId'] = question.questionId
                    Data.createData(Option, option)
