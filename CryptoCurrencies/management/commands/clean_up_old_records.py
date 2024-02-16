"""
Custom Django management command to clean up old records from the CryptoTokenRate model.
"""

from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
# pylint: disable=import-error
from CryptoCurrencies.models import CryptoTokenRate
from AvailableCurrencies.models import CurrencyExchangeRate


class Command(BaseCommand):
    """
    This command is designed to be run regularly (e.g., daily) to maintain the database
    by deleting CryptoTokenRate records that are older than 5 days. It helps in keeping
    the database size manageable and removing outdated data that is no longer relevant
    for the application's operation.
    """
    help = 'Deletes records older than 5 days'

    # pylint: disable=unused-argument
    def handle(self, *args, **kwargs):
        """
        Execute the command to delete old records from the CryptoTokenRate model.

        It calculates the threshold date (5 days before the current date and time) and
        deletes all records in the CryptoTokenRate model that are older than this date.
        """
        threshold_date = timezone.now() - timedelta(days=5)
        CryptoTokenRate.objects.filter(date__lt=threshold_date).delete()
        CurrencyExchangeRate.objects.filter(api_date_updated__lt=threshold_date).delete()
        self.stdout.write('Successfully deleted records older than 5 days.')
