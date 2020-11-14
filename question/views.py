from django.shortcuts import render

# Create your views here.
from django.views import View

from cyber_security.util.dataTools import Data
from cyber_security.util.httpTools import RestResponse
from cyber_security.util.viewsTools import NewView
from question.forms import QuestionForm
from question.models import Question, Option


class QuestionView(NewView):
    def get(self, request):
        self.userAuth()
        form = QuestionForm(self.GET())
        if not form.is_valid():
            return RestResponse.frontFail("参数错误！", form.errorsDict())
        dataList = Question.objects.filter(type=form.cleaned_data['type']).values("questionId").order_by('?')[:10]
        for data in dataList:
            print(data['questionId'])
        return RestResponse.success("获取题目成功！", {})