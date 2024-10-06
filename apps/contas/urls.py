from django.urls import path
from contas import views 

urlpatterns = [
   path('entrar/', views.login_view, name='login'), 
]