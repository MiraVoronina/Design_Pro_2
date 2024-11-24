from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register, name='register'),
    path('create-request/', views.create_request, name='create_request'),
    path('view-requests/', views.view_requests, name='view_requests'),
    path('delete-request/<int:pk>/', views.delete_request, name='delete_request'),  # Новый маршрут
]
