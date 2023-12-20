from os import getenv
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
from django.http import HttpResponse
import requests
import json
from CryptoCurrencies.models import CryptoTokenCurrency


class Command(BaseCommand):
    help = 'Added information from api to database'

    def handle(self, *args, **kwargs):
        load_dotenv()
        api_key = getenv('APIKEY_CRYPTO')
        url = 'https://min-api.cryptocompare.com/data/all/coinlist'

        list = []
        response = requests.get(url, api_key)
        try:
            content = response.json()
        except json.JSONDecodeError:
            return HttpResponse('Wrong format')
        else:
            for key, value in content.items():
                list.append(value)

            for key, value in list[2].items():
                CryptoTokenCurrency.objects.update_or_create(
                    code=key,
                    defaults={
                        'name': value['CoinName'],
                        'description': value['Description']
                    }
                )

            self.stdout.write('Crypto rate were updated')
