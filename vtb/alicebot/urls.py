from django.urls import path
from .views import alice_handler

urlpatterns = [
    path('webhook/', alice_handler, name='alice_webhook'),
]
