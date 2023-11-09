from django.contrib import admin
from django.urls import path
from django.urls import path, include
from main.views import hello_word

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('currencies/', include('AvailableCurrencies.urls')),
    path('currencypairs/', include('CurrencyPairs.urls')),
]
