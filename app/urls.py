from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.index, name= "home"),
    path("register", views.register, name= "register"),
    path("log_in", views.log_in, name= "log_in"),
    path("dashboard", views.dashboard, name= "dashboard"),
    path("log_out", views.log_out, name= "log_out"),
    path("crop_report", views.crop_report, name= "crop_report"),
    path("report", views.report, name= "report"),
    path("report1", views.report1, name= "report1"),
    path("crop_prediction", views.crop_prediction, name= "crop_prediction"),
    path("fert_rec", views.fert_rec, name= "fert_rec"),
    path("fert_report", views.fert_report, name= "fert_report"),
    path("chatbot", views.chatbot, name= "chatbot"),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
]