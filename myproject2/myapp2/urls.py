from django.urls import path
from .views import ContactListCreate

urlpatterns = [
    path('contacts/', ContactListCreate.as_view(), name='contact-list-create'),
]
