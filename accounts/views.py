import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import DesignRequest, Category


def home(request):
    """Главная страница."""
    categories = Category.objects.all()
    completed_requests = DesignRequest.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'accounts/home.html', {
        'categories': categories,
        'completed_requests': completed_requests,
        'in_progress_count': in_progress_count
    })


def login_user(request):
    """Авторизация пользователя."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'accounts/login.html')


from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.contrib import messages

def register_user(request):
    """Регистрация пользователя с автоматическим входом."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, 'Вы должны согласиться на обработку персональных данных.')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            messages.error(request, 'Логин должен содержать только латинские буквы, цифры, дефис или подчёркивание.')
            return redirect('register')

        if not re.match(r'^[а-яА-ЯёЁ\s-]+$', full_name):
            messages.error(request, 'ФИО должно содержать только кириллицу, пробелы или дефисы.')
            return redirect('register')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Некорректный формат email.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует.')
            return redirect('register')

        # Создание пользователя
        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = full_name
        user.save()

        # Автоматический вход пользователя
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу

    return render(request, 'accounts/register.html')


@login_required
def user_requests(request):
    """Просмотр заявок текущего пользователя с фильтрацией."""
    status_filter = request.GET.get('status')
    requests = DesignRequest.objects.filter(user=request.user).order_by('-created_at')
    if status_filter:
        requests = requests.filter(status=status_filter)
    return render(request, 'accounts/user_requests.html', {'requests': requests})


@login_required
def create_request(request):
    """Создание новой заявки."""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image', None)

        if not title or not description or not category_id:
            messages.error(request, 'Все поля должны быть заполнены.')
            return redirect('create_request')

        category = get_object_or_404(Category, id=category_id)

        DesignRequest.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            image=image
        )
        messages.success(request, 'Заявка успешно создана!')
        return redirect('user_requests')

    categories = Category.objects.all()
    return render(request, 'accounts/create_request.html', {'categories': categories})


@login_required
def delete_request(request, request_id):
    """Удаление заявки."""
    design_request = get_object_or_404(DesignRequest, id=request_id, user=request.user, status='new')
    design_request.delete()
    messages.success(request, 'Заявка успешно удалена.')
    return redirect('user_requests')


@staff_member_required
def update_request_status(request, request_id):
    """Смена статуса заявки администратором."""
    design_request = get_object_or_404(DesignRequest, id=request_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        comment = request.POST.get('comment')
        completed_image = request.FILES.get('completed_image', None)

        if new_status == 'in_progress' and not comment:
            messages.error(request, 'Для статуса "Принято в работу" требуется комментарий.')
            return redirect('update_request_status', request_id=request_id)

        if new_status == 'completed' and not completed_image:
            messages.error(request, 'Для статуса "Выполнено" требуется изображение.')
            return redirect('update_request_status', request_id=request_id)

        design_request.status = new_status
        design_request.comment = comment
        design_request.completed_image = completed_image
        design_request.save()
        messages.success(request, f"Статус заявки успешно изменён на {design_request.get_status_display()}.")
        return redirect('home')

    return render(request, 'accounts/update_request_status.html', {'design_request': design_request})
