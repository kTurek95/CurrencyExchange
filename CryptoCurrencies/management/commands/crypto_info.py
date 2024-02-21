"""
This module defines a Django management command
which updates cryptocurrency information in the database.
It retrieves data from an external API, processes it,
and updates or creates entries in the database for each cryptocurrency.
The command handles API responses, JSON data parsing,
and handles potential errors gracefully.
It's designed to be run as a standalone script or as part of larger Django management tasks.
"""

from os import getenv
import json
from dotenv import load_dotenv
from django.core.management.base import BaseCommand
import requests
# pylint: disable=import-error
from CryptoCurrencies.models import CryptoTokenCurrency


# pylint: disable=unused-argument
class Command(BaseCommand):
    """
    Django command to add cryptocurrency information from an API to the database.

    This command fetches data from a specified cryptocurrency API and updates
    the database with the latest information about each cryptocurrency.
    """
    help = 'Added information from api to database'

    def handle(self, *args, **kwargs):
        """
        This method is responsible for executing the command. It loads the API key,
        fetches cryptocurrency data from the API, and updates the database with
        the new information.

        Params:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        load_dotenv()
        api_key = getenv('APIKEY_CRYPTO')
        url = 'https://min-api.cryptocompare.com/data/all/coinlist'

        crypto_list = []
        response = requests.get(url, api_key, timeout=30)
        try:
            content = response.json()
        except json.JSONDecodeError:
            self.stdout.write('Wrong format')
        for key, value in content.items():
            crypto_list.append(value)

        for key, value in crypto_list[2].items():
            if value.get('Description', ''):
                CryptoTokenCurrency.objects.update_or_create(
                    code=key,
                    defaults={
                        'name': value['CoinName'],
                        'description': value['Description']
                    }
                )

        self.stdout.write('Crypto info were updated')
