from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('enter-code/', views.enter_code, name='enter_code'),
    path('profile/', views.profile, name='profile'),
]
