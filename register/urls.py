from django.urls import path
from main.views import currency_view
from .views import register

app_name = 'register'

urlpatterns = [
    path('register/', register, name='register'),
    path('', currency_view, name='home')
]