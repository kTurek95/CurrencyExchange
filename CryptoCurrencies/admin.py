from django.contrib import admin
from .models import CryptoTokenCurrency, CryptoTokenRate


class CryptoCurrenciesAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']


admin.site.register(CryptoTokenCurrency, CryptoCurrenciesAdmin)


class CryptoTokenRateAdmin(admin.ModelAdmin):
    list_display = ['token', 'rate_to_usd']


admin.site.register(CryptoTokenRate, CryptoTokenRateAdmin)
