from django.urls import path
from main.views import hello_word

urlpatterns = [
    path('', hello_word),
]