from django.core.management.base import BaseCommand
from django.http import HttpResponse
import requests
import json
from datetime import date
from AvailableCurrencies.models import CurrencyExchangeRate, AvailableCurrency


class Command(BaseCommand):
    help = 'Updated currencies rate'

    def handle(self, *args, **options):
        params = {
            'apikey': 'e0ad4966bceb4346b7949c5e3d5a6dee',
        }

        r = requests.get('https://api.currencyfreaks.com/v2.0/rates/latest', params)
        try:
            content = r.json()
        except json.JSONDecodeError:
            return HttpResponse('Wrong format')
        else:
            for code, rate in content['rates'].items():
                currency_instance = AvailableCurrency.objects.get(code=code)
                existing_rate = CurrencyExchangeRate.objects.filter(
                    currency=currency_instance,
                    api_date_updated=date.today()
                ).first()

                if not existing_rate:
                    CurrencyExchangeRate.objects.create(
                        currency=currency_instance,
                        rate_to_usd=rate,
                        api_date_updated=date.today(),
                        user_id=1
                    )

        self.stdout.write('Currencies rate were updated')