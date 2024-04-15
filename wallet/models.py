from django.db import models
from django.contrib.auth.models import User
from AvailableCurrencies.models import AvailableCurrency
from CryptoCurrencies.models import CryptoTokenCurrency


class Wallet(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='wallets')
    balance = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.ForeignKey(AvailableCurrency, on_delete=models.SET_NULL, null=True, blank=True)
    crypto_currency = models.ForeignKey(CryptoTokenCurrency, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.currency:
            return f'Currency wallet'
        else:
            return 'Crypto wallet'


class Transaction(models.Model):
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='users', default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    BUY = 'BUY'
    SELL = 'SELL'
    TRANSACTION_TYPE_CHOICES = [
        (BUY, 'Purchase'),
        (SELL, 'Sale'),
    ]
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES,
    )

    purchased_currency = models.CharField(max_length=10, blank=False, null=True)

    COMPLETED = 'COMPLETED'
    IN_PROGRESS = 'IN_PROGRESS'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (IN_PROGRESS, 'In Progress'),
        (REJECTED, 'Rejected'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    value_in_USD = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    balance_after_transaction = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    date = models.DateTimeField()
