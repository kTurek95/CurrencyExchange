from django.urls import path
from .views import currencies, currencies_list

urlpatterns = [
    path('', currencies),
    path('list/', currencies_list)
]