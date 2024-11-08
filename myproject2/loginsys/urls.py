from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Используем встроенное представление для выхода
    path('enter-code/', views.enter_code, name='enter_code'),
    path('profile/', views.profile, name='profile'),
]
