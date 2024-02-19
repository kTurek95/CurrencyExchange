from os import getenv
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.http import HttpResponse
import requests
import json
from dotenv import load_dotenv
from AvailableCurrencies.models import AvailableCurrency


class Command(BaseCommand):
    help = 'Added information from api to database'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID użytkownika')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User does not exists'))
        load_dotenv()
        api_key = getenv('APIKEY_CURRENCIES')
        params = {
            'apikey': api_key,
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
                        'image': currency_data.get('icon'),
                        'user': user
                    }
                )

            self.stdout.write('Currencies rate were updated')