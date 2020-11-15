
# Create your views here.
import json

from cyber_security.util.dataTools import Data
from cyber_security.util.httpTools import RestResponse
from cyber_security.util.viewsTools import NewView
from question.forms import QuestionForm, QuestionByIdForm
from question.models import Question, Option

# 获取题目
from user.models import User


class QuestionView(NewView):
    def get(self, request):
        self.userAuth()
        form = QuestionForm(self.GET())
        if not form.is_valid():
            return RestResponse.frontFail("参数错误！", form.errorsDict())
        data = form.cleaned_data
        data['questionNum'] = 10 if not data['questionNum'] else data['questionNum']
        dataList = Question.objects.filter(type=data['type']).values("questionId").order_by('?')[:data['questionNum']]
        questionIdList = list(map(lambda x: x['questionId'], dataList))
        questionList = Data.getDataList(Question, questionIdList)
        if data['type'] in [2, 3]:  # 单选题和多选题
            optionIdList = Option.objects.filter(questionId__in=questionIdList).values('optionId')
            optionIdList = list(map(lambda x: x['optionId'], optionIdList))
            optionList = Data.getDataList(Option, optionIdList)
            questionOptionDict = {}
            for option in optionList:
                if option['questionId'] not in questionOptionDict:
                    questionOptionDict[option['questionId']] = []
                questionOptionDict[option['questionId']].append(option)
            for question in questionList:
                question['optionList'] = questionOptionDict[question['questionId']]
        return RestResponse.success("获取题目成功！", {"questionList": questionList})

# 答题判断
class QuestionByIdView(NewView):
    def post(self, request, questionId):
        self.userAuth()
        form = QuestionByIdForm(self.POST())
        if not form.is_valid():
            return RestResponse.frontFail("参数错误！", form.errorsDict())
        data = form.cleaned_data
        answerList = json.loads(data['answerList']) if data['answerList'] else []
        question = Data.getData(Question, questionId)
        if question['type'] == 1:
            if len(answerList) != 1:
                return RestResponse.userFail("回答错误！")
            ques = Question.objects.filter(questionId=questionId).values('isCorrect').first()
            if not ques or ques['isCorrect'] != answerList[0]:
                return RestResponse.userFail("回答错误！")
        elif question['type'] == 2:
            if len(answerList) != 1:
                return RestResponse.userFail("回答错误！")
            option = Option.objects.filter(**{'optionId': answerList[0]}).values(*['questionId', 'isCorrect']).first()
            if option['questionId'] != int(questionId) or option['isCorrect'] != 1:
                return RestResponse.userFail("回答错误！")
        elif question['type'] == 3:
            if len(answerList) < 2:
                return RestResponse.userFail("回答错误！")
            optionList = Option.objects.filter(**{'questionId': questionId, 'isCorrect': 1}).values('optionId')
            if set(map(lambda x: x['optionId'], optionList)) != set(answerList):
                return RestResponse.userFail("回答错误！")
        data = Data.getData(User, self.userId)
        Data.updateData(User, {"userId": self.userId, "score": data['score'] + question['type']*5})
        return RestResponse.success("回答正确!", {"score": question['type']*5})