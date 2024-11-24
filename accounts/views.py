from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

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
