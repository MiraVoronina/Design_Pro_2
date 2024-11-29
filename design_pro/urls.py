from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('superadmin/', admin.site.urls),
    path('', include('accounts.urls')),  # Основные маршруты
    path('catalog/', lambda request: redirect('home')),  # Перенаправление /catalog/ на главную
]
