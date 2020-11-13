from django.shortcuts import render

# Create your views here.
from django.views import View

from cyber_security.util.dataTools import Data
from question.models import Question


class TestView(View):
    def get(self, request):
        print('+++')
        try:
            s = Data.getData(Question, 1)
        except Exception as e:
            print(e)
        print(s)
        # Data.createData(Question, None)
        print("...")