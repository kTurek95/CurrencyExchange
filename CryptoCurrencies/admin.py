from django.contrib import admin
from .models import CryptoTokenCurrency


class CryptoCurrenciesAdmin(admin.ModelAdmin):
    pass


admin.site.register(CryptoTokenCurrency, CryptoCurrenciesAdmin)
