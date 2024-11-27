from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import DesignRequest

def home(request):
    """Главная страница."""
    completed_requests = DesignRequest.objects.filter(status='completed').order_by('-created_at')[:4]
    in_progress_count = DesignRequest.objects.filter(status='in_progress').count()
    return render(request, 'accounts/home.html', {
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

def register_user(request):
    """Регистрация пользователя с согласием на обработку персональных данных."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        agree = request.POST.get('agree')

        if not agree:
            messages.error(request, 'Вы должны согласиться на обработку персональных данных.')
            return redirect('register')

        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует.')
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        messages.success(request, 'Регистрация успешна. Теперь вы можете войти.')
        return redirect('login')

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
        category = request.POST.get('category')
        image = request.FILES.get('image', None)

        if not title or not description or not category:
            messages.error(request, 'Все поля должны быть заполнены.')
            return redirect('create_request')

        DesignRequest.objects.create(
            user=request.user,
            title=title,
            description=description,
            category=category,
            image=image
        )
        messages.success(request, 'Заявка успешно создана!')
        return redirect('user_requests')

    return render(request, 'accounts/create_request.html')

@staff_member_required
def update_request_status(request, request_id):
    """Смена статуса заявки администратором."""
    design_request = get_object_or_404(DesignRequest, id=request_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        design_request.status = new_status
        design_request.save()
        messages.success(request, f"Статус заявки успешно изменён на {design_request.get_status_display()}.")
        return redirect('home')
    return render(request, 'accounts/update_request_status.html', {'design_request': design_request})
