from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, SecretCodeForm
from .models import CustomUser


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('enter_code')  # Перенаправляем на страницу ввода кода
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def enter_code(request):
    if request.method == 'POST':
        form = SecretCodeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            if request.user.secret_code == code:
                return redirect('profile')  # Успешное подтверждение
    else:
        form = SecretCodeForm()
    return render(request, 'enter_code.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')
