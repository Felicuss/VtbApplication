from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.register, name='register1'),
    path('register/', views.register, name='register2'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Используем встроенное представление для выхода
    path('enter-code/', views.enter_code, name='enter_code'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='profile'),
]
