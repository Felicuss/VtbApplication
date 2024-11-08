from django.contrib import admin
from django.urls import path, include
# маршруты URL для всего проекта
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp2.urls')),
    path('', include('loginsys.urls')),
]
