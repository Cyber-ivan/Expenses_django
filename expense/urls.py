from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import Register, Home


urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('register/', Register.as_view(), name='register'),  # Регистрация
    path('home/', Home.as_view(), name='test'),  # Пример маршрута для Test
    path('', include('django.contrib.auth.urls')),  # Для логина, логаута и т.д.
]