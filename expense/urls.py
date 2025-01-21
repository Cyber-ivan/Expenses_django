from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from .views import Register

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('django.contrib.auth.urls')),
    path('/register', Register.as_view(), name='register'),
]
