
# Create your views here.

from cyber_security.util.dataTools import Data
from cyber_security.util.httpTools import RestResponse
from cyber_security.util.viewsTools import NewView
from question.forms import QuestionForm
from question.models import Question, Option

# 获取题目
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
            optionList = Option.objects.filter(questionId__in=questionIdList).values(*Option.allowFields())
            questionOptionDict = {}
            for option in optionList:
                if option['questionId'] not in questionOptionDict:
                    questionOptionDict[option['questionId']] = []
                questionOptionDict[option['questionId']].append(option)
            for question in questionList:
                question['optionList'] = questionOptionDict[question['questionId']]
        return RestResponse.success("获取题目成功！", {"questionList": questionList})