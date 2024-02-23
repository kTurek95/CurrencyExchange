"""
This module contains a Django management command used for updating
the exchange rates of cryptocurrencies in the database.
The command fetches current exchange rate data for each cryptocurrency
listed in the CryptoTokenCurrency model from an external API.
This data includes the exchange rates against USD.
The command updates existing records or creates new ones
in the CryptoTokenRate model with the latest rates.
It also handles errors and exceptions that may occur during the data retrieval
process and removes cryptocurrencies from the database if they are no longer supported by the API.
"""


from datetime import date
from os import getenv
from tqdm import tqdm
from django.core.management.base import BaseCommand
import requests
from dotenv import load_dotenv
# pylint: disable=import-error
from CryptoCurrencies.models import CryptoTokenCurrency, CryptoTokenRate


# pylint:disable=unused-argument
class Command(BaseCommand):
    """
    This Django management command updates cryptocurrency rates in the database.
    It fetches the latest exchange rates for cryptocurrencies against USD from an external API
    """
    help = "Added crypto rate compare to database"

    def handle(self, *args, **kwargs):
        """
        The handle method executes the main logic of the command.
        It loads the environment variables, retrieves API keys, iterates over each
        cryptocurrency, and fetches its current rate against USD. If the rate is valid,
        it updates or creates a new record in the database. Errors during the fetch process
        are handled gracefully, and unsupported currencies are marked for removal.
        """
        load_dotenv()
        api_key = getenv('APIKEY_CRYPTO')

        currencies_to_remove = []

        currencies = CryptoTokenCurrency.objects.all()
        for crypto in tqdm(currencies):
            try:
                response = requests.get(
                    url=f'https://min-api.cryptocompare.com/data/price?fsym='
                        f'{crypto}&tsyms=USD&api_key={api_key}',
                    timeout=30)
                response.raise_for_status()
                content = response.json()
                if 'Response' in content and content['Response'] == 'Error':
                    self.stderr.write(f"Error for {crypto.code}: {content['Message']}")
                    if crypto.id is not None:
                        currencies_to_remove.append(crypto)
                    continue
                if 'USD' not in content:
                    rate_to_usd = 0
                else:
                    rate_to_usd = round(content['USD'], 5)

                if rate_to_usd != 0:
                    existing_record \
                        = CryptoTokenRate.objects.filter(token=crypto, date=date.today()).first()
                    if not existing_record:
                        CryptoTokenRate.objects.create(
                            token=crypto,
                            rate_to_usd=rate_to_usd,
                            date=date.today()
                        )
            except requests.exceptions.Timeout:
                self.stderr.write('Timeout')
            except requests.exceptions.RequestException as e:
                self.stderr.write(f"Error: {str(e)}")
            # pylint: disable=broad-exception-caught
            except Exception as e:
                self.stderr.write(f"Error: {str(e)}")

        for currency in currencies_to_remove:
            currency.delete()

        self.stdout.write('Crypto rate were updated')
