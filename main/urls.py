from django.urls import path
from main.views import currency_view

app_name = 'main'

urlpatterns = [
    path('', currency_view, name='currency'),
]