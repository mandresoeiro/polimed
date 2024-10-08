from django.urls import path
from contas import views
from django.shortcuts import render

urlpatterns = [
    path('timeout/',  views.timeout_view, name='timeout'),
    path('entrar/', views.login_view, name='login'),
    path('criar-conta/', views.register_view, name='register'),


]
