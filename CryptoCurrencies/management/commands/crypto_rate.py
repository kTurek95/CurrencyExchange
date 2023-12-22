from datetime import date
from os import getenv

from django.core.management.base import BaseCommand
import requests
from dotenv import load_dotenv

from CryptoCurrencies.models import CryptoTokenCurrency, CryptoTokenRate


class Command(BaseCommand):
    help = "Added crypto rate compare to database"

    def handle(self, *args, **kwargs):
        load_dotenv()
        api_key = getenv('APIKEY_CRYPTO')

        currencies = CryptoTokenCurrency.objects.all()
        for crypto in currencies:
            try:
                response = requests.get(
                    url=f'https://min-api.cryptocompare.com/data/price?fsym={crypto}&tsyms=USD&api_key={api_key}',
                    timeout=5)
                response.raise_for_status()
                content = response.json()
                if 'Response' in content and content['Response'] == 'Error':
                    self.stderr.write(f"Error for {crypto}: {content['Message']}")
                    continue
                if 'USD' not in content:
                    rate_to_usd = 0
                else:
                    rate_to_usd = round(content['USD'], 5)

                if rate_to_usd != 0:
                    existing_record = CryptoTokenRate.objects.filter(token=crypto, date=date.today()).first()
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
            except Exception as e:
                self.stderr.write(f"Error: {str(e)}")

        self.stdout.write('Crypto rate were updated')