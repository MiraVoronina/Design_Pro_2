from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('superadmin/', admin.site.urls),  # Панель администратора доступна по адресу /superadmin
    path('', include('accounts.urls')),  # Маршруты приложения accounts
]
