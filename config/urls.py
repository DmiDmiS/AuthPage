# config/urls.py
from django.contrib import admin
from django.urls import path, include # Убедитесь, что include импортирован!

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')), # Точно ли тут имя вашего приложения?
]

