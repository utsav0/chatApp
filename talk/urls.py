from django.http import JsonResponse
from django.urls import path
from . import views


urlpatterns = [
    path("", views.everyone, name="everyone page"),
    path("search", views.search, name="search"),
    path("chat", views.chat, name="chat"),
    path("addMsgToDB", views.addMsgToDB, name="add new messages to db"),
    path("checkNewMsg", views.checkNewMsg, name="check new messages"),
    path("loginErr", views.loginErr, name = "login error"),
    path("logout", views.logout, name = "logout function"),
]
