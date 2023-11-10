from django.urls import path
from .views import currencies, currencies_list, currencies_details

app_name = 'currencies'

urlpatterns = [
    path('test', currencies),
    path('', currencies_list, name='list'),
    path('<int:currency_id>', currencies_details, name='details')
]