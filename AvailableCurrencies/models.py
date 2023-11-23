from django.db import models
from django.contrib.auth.models import User


class AvailableCurrency(models.Model):
    name = models.CharField(max_length=255, null=True)
    code = models.CharField(max_length=5)
    country_code = models.CharField(max_length=5, null=True)
    country_name = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255)

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='AvailableCurrency')
    example_file = models.FileField(upload_to='AvailableCurrencies/examples/', blank=True, null=True)
    image = models.ImageField(upload_to='app/images')

    def __str__(self):
        return f'{self.code} - {self.name}'


class CurrencyExchangeRate(models.Model):
    currency = models.ForeignKey(AvailableCurrency, on_delete=models.CASCADE)
    rate_to_usd = models.CharField(max_length=255)
    api_date_updated = models.DateField()

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='CurrencyExchangeRate')

    def __str__(self):
        return f'{self.currency.code} - {self.rate_to_usd}'