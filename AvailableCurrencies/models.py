from django.db import models
from django.contrib.auth.models import User


class AvailableCurrency(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=4)

    def __str__(self):
        return f'{self.code} - {self.name} '