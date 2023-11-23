from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from .models import AvailableCurrency, CurrencyExchangeRate


class CurrencyResource(resources.ModelResource):
    class Meta:
        model = AvailableCurrency


class AvailableCurrenciesAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ['code', 'name', 'country_name']
    search_fields = ['code']
    resource_class = CurrencyResource
    list_filter = ['country_name']


admin.site.register(AvailableCurrency, AvailableCurrenciesAdmin)


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['currency_id', 'rate_to_usd']


admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)
