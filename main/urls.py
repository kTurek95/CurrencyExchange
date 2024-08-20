from django.urls import path
from main.views import currency_view, calculate

app_name = 'main'

urlpatterns = [
    path('', currency_view, name='currency'),
    path('calculate/', calculate, name='calculate')
]