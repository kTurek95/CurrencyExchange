from django.db import models


class CryptoTokenCurrency(models.Model):
    code = models.CharField(max_length=6)
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=255, null=True)