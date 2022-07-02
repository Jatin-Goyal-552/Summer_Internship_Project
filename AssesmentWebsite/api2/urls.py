from django.urls import path
from . import views

urlpatterns=[
    path('demographic/', views.demographic, name='demographic'),
    path('demographic/<pk>', views.demographic, name='demographic2'),
    path('expertise/', views.expertise, name='expertise'),
    path('expertise/<pk>', views.expertise, name='expertise2'),
    path('login/', views.login1, name='login'),
    path('questionbank/', views.questionbank, name='questionbank'),
    path('questionbank/<pk>', views.questionbank, name='questionbank2'),
    path('questionbanklevel/', views.questionbanklevel, name='questionbanklevel'),
    path('questionbanklevel/<pk>', views.questionbanklevel, name='questionbanklevel2'),
    path('code/', views.code, name='code'),
    path('code/<pk>', views.code, name='code2'),
    path('question/', views.question, name='question'),
    path('question/<pk>', views.question, name='question2'),
    path('evaluation/', views.evaluation, name='evaluation'),
    path('evaluation/<pk>', views.evaluation, name='evaluation2'),
    path('score/', views.score, name='score'),
    path('score/<pk>', views.score, name = 'score2'),
    path('download/', views.download, name = 'download'),
    path('getcode/', views.getcode, name = 'getcode'),
    path('getquestion/', views.getquestion, name = 'getquestion'),
    path('time/', views.time, name='time'),
    path('time/<pk>', views.time, name='time2')
]