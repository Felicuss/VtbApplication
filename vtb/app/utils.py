from django.shortcuts import redirect
from django.urls import reverse

def redirect_if_unauthenticated(view_func):
    def wrapper(request, *args, **kwargs):
        # Проверяем аутентификацию пользователя
        if not request.user.is_authenticated:
            # Разрешаем доступ к login и register
            allowed_paths = [reverse('login'), reverse('register')]
            if request.path not in allowed_paths:
                return redirect('register')
        return view_func(request, *args, **kwargs)
    return wrapper
