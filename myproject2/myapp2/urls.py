from django.urls import path
from .views import ContactListCreate
from .views import yandex_handler

urlpatterns = [
    path('contacts/', ContactListCreate.as_view(), name='contact-list-create'),
    path('yandex_alice/', yandex_handler, name='yandex_handler')
]
