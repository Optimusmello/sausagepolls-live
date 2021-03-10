from django.contrib import admin
from django.urls import path,include
from PollApp import views

urlpatterns = [
    path('',views.home,name='home'),
    path('addpoll/',views.AddPoll,name='addpoll'),
    path('polls/<int:poll_id>/',views.polls,name='polls'),
    path('polls/<int:poll_id>/result/',views.result,name='result'),
    path('polls/<int:poll_id>/edit/',views.PollQuestionEdit,name='question_edit'),
    path('polls/<int:poll_id>/delete/',views.PollDelete,name='poll_delete'),
]
