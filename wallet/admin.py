from django.contrib import admin

from wallet.models import Wallet, Transaction


class WalletAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wallet, WalletAdmin)


class TransactionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Transaction, WalletAdmin)