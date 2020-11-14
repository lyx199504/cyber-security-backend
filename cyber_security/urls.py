"""cyber_security URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from question.views import QuestionView
from user.views import UserLoginView, UserSelfView, UserCheckinView

urlpatterns = [
    path('admin/', admin.site.urls),

    # 用户接口
    path('user/login', UserLoginView.as_view()),
    path('user/self', UserSelfView.as_view()),
    path('user/checkin', UserCheckinView.as_view()),

    # 答题接口
    path('question', QuestionView.as_view()),
]
