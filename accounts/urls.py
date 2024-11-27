from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Главная страница
    path('login/', views.login_user, name='login'),  # Авторизация
    path('register/', views.register_user, name='register'),  # Регистрация
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Выход
    path('requests/', views.user_requests, name='user_requests'),  # Просмотр заявок
    path('requests/create/', views.create_request, name='create_request'),  # Создание заявки
    path('requests/<int:request_id>/delete/', views.delete_request, name='delete_request'),  # Удаление заявки
    path('requests/<int:request_id>/update/', views.update_request_status, name='update_request_status'),  # Смена статуса
]
