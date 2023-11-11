from django.contrib import admin
from .models import AvailableCurrency


class AvailableCurrenciesAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code']
    list_filter = ['code']


admin.site.register(AvailableCurrency, AvailableCurrenciesAdmin)
