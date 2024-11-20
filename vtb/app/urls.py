from django.conf.urls import handler404, handler500
from .views import custom_404, custom_500
from django.urls import path
from .views import (
    register_view,
    login_view,
    profile_view,
    logout_view,
    waiting_for_confirmation_view,
    check_made_2fa_view,
    regenerate_key
)

urlpatterns = [
    path('', profile_view, name='profile2'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('waiting-for-confirmation/', waiting_for_confirmation_view, name='waiting_for_confirmation'),
    path('check-made-2fa/', check_made_2fa_view, name='check_made_2fa'),
    path('regenerate-key/', regenerate_key, name='regenerate_key'),
]
handler404 = custom_404
handler500 = custom_500
