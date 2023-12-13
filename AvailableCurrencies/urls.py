from django.urls import path
from .views import currencies, currencies_list, currencies_details, currencies_rate, compare_previous_day_rate

app_name = 'currencies'

urlpatterns = [
    path('test', currencies),
    path('list/', currencies_list, name='list'),
    path('<int:currency_id>', currencies_details, name='details'),
    path('rate/', currencies_rate, name='rate'),
    path('compare/', compare_previous_day_rate, name='compare_rate')
]