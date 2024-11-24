from django.contrib import admin
from django.urls import path, include
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('catalog/', views.home, name='home'),  # Главная страница для /catalog/
    path('accounts/', include('accounts.urls')),  # Подключение приложения accounts
]
