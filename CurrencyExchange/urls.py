from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from dotenv import load_dotenv
import os

load_dotenv()
admin_url = os.environ.get('DJANGO_ADMIN_URL', 'admin/')

urlpatterns = [
    path(f'{admin_url}/', admin.site.urls),
    path('currencies/', include('AvailableCurrencies.urls')),
    path('currencypairs/', include('CurrencyPairs.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('crypto/', include('CryptoCurrencies.urls')),
    path('wallet/', include('wallet.urls')),
    # path('tinymce/', include('tinymce.urls')),
    path('', include('main.urls')),
    path('', include('register.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
