# authentication/urls.py
from django.urls import path
from .views import login_view, health_check, cpu_stress, home_view

urlpatterns = [
   
    path('', home_view, name='home'),
    path('api/login', login_view, name='login'),
    path('health', health_check, name='health'),
    path('load', cpu_stress, name='load'),
]

