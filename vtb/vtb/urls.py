from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('alicebot/', include('alicebot.urls')),
]

handler404 = 'app.views.custom_404'
handler400 = 'app.views.custom_400'
handler500 = 'app.views.custom_500'