from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, SecretCodeForm
from .models import UserSecretCode

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Создаем `UserSecretCode` с пустым `secret_code`
            UserSecretCode.objects.create(user=user)

            login(request, user)
            return redirect('profile')  # перенаправляем в профиль сразу после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def enter_code(request):
    if request.method == 'POST':
        form = SecretCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                if request.user.usersecretcode.secret_code == code:
                    return redirect('profile')
            except UserSecretCode.DoesNotExist:
                form.add_error(None, "No secret code found for this user.")
    else:
        form = SecretCodeForm()
    return render(request, 'enter_code.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')


from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Проверка на наличие `secret_code`
            try:
                if user.usersecretcode.secret_code:  # Если `secret_code` заполнен
                    return redirect('enter_code')
            except UserSecretCode.DoesNotExist:
                pass  # Если у пользователя нет `UserSecretCode`, пропускаем

            # Переход в профиль, если `secret_code` пуст
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

