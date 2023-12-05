from django.db import models


class CryptoTokenCurrency(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.code


class CryptoTokenRate(models.Model):
    token = models.ForeignKey(CryptoTokenCurrency, on_delete=models.CASCADE)
    rate_to_usd = models.CharField(max_length=10)
    date = models.DateField()
