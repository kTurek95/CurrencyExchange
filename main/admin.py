from django.contrib import admin
from main.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)

# admin.site.index_template = 'admin/includes/base_site.html'
admin.site.site_header = 'CurrencyExchange app'