from django.urls import path
from main.views import hello_word
from .views import register

app_name = 'register'

urlpatterns = [
    path('register/', register, name='register'),
    path('', hello_word, name='home')
]