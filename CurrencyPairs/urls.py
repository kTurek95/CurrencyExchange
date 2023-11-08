from django.urls import path
from .views import currency_pairs, pairs_list

urlpatterns = [
    path('', currency_pairs),
    path('list/', pairs_list)
]