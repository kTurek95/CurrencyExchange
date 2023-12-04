from django.core.management.base import BaseCommand
from django.http import HttpResponse
import requests
import json
from AvailableCurrencies.models import AvailableCurrency


class Command(BaseCommand):
    help = 'Added information from api to database'

    def handle(self, *args, **kwargs):
        params = {
            'apikey': 'e0ad4966bceb4346b7949c5e3d5a6dee',
        }

        r = requests.get('https://api.currencyfreaks.com/v2.0/supported-currencies', params)
        try:
            content = r.json()
        except json.JSONDecodeError:
            return HttpResponse('Wrong format')
        else:
            for currency_key in content["supportedCurrenciesMap"]:
                currency_data = content["supportedCurrenciesMap"][currency_key]

                status_bool = currency_data['status'] == 'AVAILABLE'

                AvailableCurrency.objects.update_or_create(
                    code=currency_data['currencyCode'],
                    defaults={
                        'name': currency_data['currencyName'],
                        'country_code': currency_data.get('countryCode', ''),
                        'country_name': currency_data.get('countryName', ''),
                        'status': status_bool,
                        'image': currency_data.get('icon')
                    }
                )

            self.stdout.write('Currencies rate were updated')