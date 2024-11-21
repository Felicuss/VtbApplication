from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserInfo
from .utils import redirect_if_unauthenticated
import secrets
from cryptography.fernet import Fernet
from django.contrib.auth.models import User
from .telegram_notifications import send_message_to_user

from django.http import JsonResponse

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


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            user_info = UserInfo.objects.get(user=user)
            if not user_info.has_yandex_2fa:
                login(request, user)
                if user_info.telegram_username:
                    send_message_to_user(
                        username=user_info.telegram_username,
                        message=f"Внимание, в ваш аккаунт только что совершили вход. "
                                f"Если это были не вы срочно измените пароль."
                    )
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
                if user_info.telegram_username:
                    send_message_to_user(
                        username=user_info.telegram_username,
                        message=f"Внимание, в ваш аккаунт только что совершили вход. "
                                f"Если это были не вы срочно измените пароль."
                    )
                user_info.made_2fa = False
                user_info.save()
                return JsonResponse({'redirect': True})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Пользователь не найден.'}, status=404)
        except UserInfo.DoesNotExist:
            return JsonResponse({'error': 'Информация о пользователе не найдена.'}, status=404)
    return JsonResponse({'redirect': False})


@redirect_if_unauthenticated
@login_required
def profile_view(request):
    user_info = decrypt_key(UserInfo.objects.get(user=request.user).secret_key)
    user = UserInfo.objects.get(user=request.user)
    if user.has_yandex_2fa and user.telegram_username != '':
        percent = 100
        text = 'Ваш уровень защиты максимальный'
        color_bg = 'green'
        color_text = 'white'
    elif not user.has_yandex_2fa and user.telegram_username != '':
        percent = 38
        text = 'Уровень защиты аккаунта низкий. Пожалуйста подключите 2FA через Яндекс Алису.'
        color_bg = 'yellow'
        color_text = 'black'
    elif user.has_yandex_2fa and user.telegram_username == '':
        percent = 80
        text = ('Уровень защиты аккаунта высокий. '
                'Подключите уведомления в телеграмме о входе в ваш аккаунт в настройках.')
        color_bg = 'green'
        color_text = 'white'
    else:
        percent = 18
        text = ('Уровень защиты аккаунта минимальный. '
                'Подключите 2FA через Яндекс Алису и уведомления в телеграмме о входе в ваш аккаунт в настройках')
        color_bg = 'red'
        color_text = 'white'
    context = {
        'percent' : percent,
        'text': text,
        'color_bg': color_bg,
        'color_text': color_text,
        'user_info': user_info,

    }
    return render(request, 'profile.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


from django.shortcuts import redirect

def custom_404(request, exception):
    return redirect('/register')

def custom_400(request, exception):
    return redirect('/register')

def custom_500(request):
    return redirect('/register')

def custom_504(request):
    return redirect('/register')



def generate_key():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    key = ''.join(secrets.choice(characters) for _ in range(8))
    return key


@login_required
def regenerate_key(request):
    if request.method == 'POST':
        user = request.user
        new_key = generate_key()
        hashed_key = hash_key(new_key)
        UserInfo.objects.update_or_create(user=user, defaults={'secret_key': hashed_key, 'has_yandex_2fa': False})

        return JsonResponse({'new_secret_key': new_key})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@redirect_if_unauthenticated
@login_required
def settings_view(request):
    user_info, created = UserInfo.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        tg_username = request.POST.get('tg_username', '').strip()
        user_info.telegram_username = tg_username
        user_info.save()
    return render(request, 'settings.html', {'user_info': user_info})


