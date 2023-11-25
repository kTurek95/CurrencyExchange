from django.contrib import admin
from .models import CurrencyPair


class CurrencyPairsAdmin(admin.ModelAdmin):
    list_display = ['code', 'name']
    search_fields = ['code']
    list_filter = ['code']


admin.site.register(CurrencyPair, CurrencyPairsAdmin)
