# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница по пути ''
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
]
