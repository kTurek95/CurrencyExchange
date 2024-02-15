from django.db import models


class CryptoTokenCurrency(models.Model):
    code = models.CharField(max_length=15)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=5000, null=True)

    def __str__(self):
        return self.code


class CryptoTokenRate(models.Model):
    token = models.ForeignKey(CryptoTokenCurrency, on_delete=models.CASCADE)
    rate_to_usd = models.CharField(max_length=20)
    date = models.DateField()

    @staticmethod
    def scientific_notation_number(mantissa, exponent):
        return mantissa * (10 ** exponent)

    def __str__(self):
        if 'e' in self.rate_to_usd:
            number = self.rate_to_usd.split('-')
            result = self.scientific_notation_number(float(number[0].split('e')[0]), -1 * int(number[1]))
            return f'{self.token.name}: {round(result, 6)}'
        else:
            return self.token.name + ': ' + self.rate_to_usd + '$'

