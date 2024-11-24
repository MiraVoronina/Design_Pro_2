from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from .forms import DesignRequestForm

def home(request):
    return render(request, 'accounts/home.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'accounts/login.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        agree = request.POST.get('agree')

        # Server-side validations
        if password != password2:
            messages.error(request, 'Пароли не совпадают.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Логин уже занят.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email уже зарегистрирован.')
        elif not agree:
            messages.error(request, 'Вы должны согласиться с обработкой персональных данных.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name,
            )
            user.save()
            messages.success(request, 'Вы успешно зарегистрированы.')
            return redirect('login')
    return render(request, 'accounts/register.html')

@login_required
def create_request(request):
    if request.method == 'POST':
        form = DesignRequestForm(request.POST, request.FILES)
        if form.is_valid():
            design_request = form.save(commit=False)
            design_request.user = request.user  # Привязка к текущему пользователю
            design_request.save()
            return redirect('view_requests')  # Перенаправление на страницу просмотра заявок
    else:
        form = DesignRequestForm()
    return render(request, 'accounts/create_request.html', {'form': form})

@login_required
def view_requests(request):
    status_filter = request.GET.get('status')  # Получаем выбранный статус из запроса
    requests = request.user.design_requests.all()  # Все заявки пользователя

    if status_filter in ['new', 'in_progress', 'completed']:  # Проверяем валидные статусы
        requests = requests.filter(status=status_filter)

    return render(request, 'accounts/view_requests.html', {
        'requests': requests,           # Отфильтрованные заявки
        'status_filter': status_filter, # Выбранный статус
    })

@login_required
def delete_request(request, pk):
    design_request = get_object_or_404(request.user.design_requests, pk=pk)
    if design_request.status != 'new':
        return HttpResponseForbidden("Нельзя удалить заявку, которая уже в работе или завершена.")
    if request.method == 'POST':
        design_request.delete()
        return redirect('view_requests')
    return render(request, 'accounts/delete_request.html', {'design_request': design_request})
