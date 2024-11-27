from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Административная панель Django
    path('', include('accounts.urls')),  # Подключение маршрутов из приложения accounts
]
