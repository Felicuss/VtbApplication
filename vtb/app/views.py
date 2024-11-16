from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo
import secrets
from cryptography.fernet import Fernet

secret_key = b'gnehx6C8O2o2JquonBEzPVrDGfdnRns8K34zzkqiPi8='


def hash_key(key):
    f = Fernet(secret_key)
    encrypted_key = f.encrypt(key.encode())
    return encrypted_key.decode()


def decrypt_key(encrypted_key):
    f = Fernet(secret_key)
    decrypted_key = f.decrypt(encrypted_key.encode())
    return decrypted_key.decode()


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_info = UserInfo.objects.get(user=user)
            if not user_info.has_yandex_2fa:
                login(request, user)
                return redirect('profile')
            else:
                request.session['waiting_for_confirmation'] = True
                request.session['user_id'] = user.id
                return redirect('waiting_for_confirmation')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def waiting_for_confirmation_view(request):
    if 'waiting_for_confirmation' not in request.session:
        return redirect('login')
    return render(request, 'waiting_for_confirmation.html')


from django.contrib.auth.models import User


def check_made_2fa_view(request):
    user_id = request.session.get('user_id')
    if user_id is not None:
        try:
            user = User.objects.get(id=user_id)
            user_info = UserInfo.objects.get(user=user)
            if user_info.made_2fa:
                del request.session['waiting_for_confirmation']
                del request.session['user_id']
                login(request, user)
                user_info.made_2fa = False
                user_info.save()
                return JsonResponse({'redirect': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден.'}, status=404)
        except UserInfo.DoesNotExist:
            return JsonResponse({'error': 'Информация о пользователе не найдена.'}, status=404)
    return JsonResponse({'redirect': False})


@login_required
def profile_view(request):
    user_info = decrypt_key(UserInfo.objects.get(user=request.user).secret_key)
    return render(request, 'profile.html', {'user_info': user_info})


def logout_view(request):
    logout(request)
    return redirect('login')