from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('currencies/', include('AvailableCurrencies.urls')),
    path('currencypairs/', include('CurrencyPairs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('test', include('CryptoCurrencies.urls')),
    path('', include('main.urls')),
    path('', include('register.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
