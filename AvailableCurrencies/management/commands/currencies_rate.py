from django.core.management.base import BaseCommand
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from django.utils import timezone
import requests
import json
import datetime
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
                api_date_str = content.get('date')
                api_date = parse_date(api_date_str) if api_date_str else timezone.now().date()
                if not isinstance(api_date, datetime.date):
                    api_date = timezone.now().date()
                CurrencyExchangeRate.objects.update_or_create(
                    currency=currency_instance,
                    defaults={'rate_to_usd': rate,
                              'api_date_updated': api_date}
                )

        self.stdout.write('Currencies rate were updated')