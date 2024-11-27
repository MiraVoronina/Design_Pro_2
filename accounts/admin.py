from django.contrib import admin

# Register your models here.
# accounts/admin.py
from django.contrib import admin
from .models import DesignRequest

@admin.register(DesignRequest)
class DesignRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')  # Поля, которые будут отображаться в списке заявок
    list_filter = ('status', 'category')  # Фильтры для панели администратора
    search_fields = ('title', 'description', 'category')  # Поля для поиска
    ordering = ('-created_at',)  # Сортировка по дате создания
