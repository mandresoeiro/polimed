from django.urls import path, include
from contas import views


urlpatterns = [
    path("", include("django.contrib.auth.urls")),  # Django auth
    path('timeout/',  views.timeout_view, name='timeout'),
    path('sair/', views.logout_view, name='logout'),
    path('entrar/', views.login_view, name='login'),
    path('criar-conta/', views.register_view, name='register'),


]


# TODO EXEMPLE DE URLS
#     from django.contrib.auth import views as auth_views
#     #Para não confundir com views do django apelida de auth_views

#     urlpatterns = [
#         "chances-password/", auth_views.PasswordChangeView.as_view(),
# template_name="chances-password.html"),
#     ]
