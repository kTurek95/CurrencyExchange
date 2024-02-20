from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Cleans a specified database table and reset its ID sequence'

    def add_arguments(self, parser):
        parser.add_argument('app_label', type=str, help='Label of the app')
        parser.add_argument('model_name', type=str, help='Name of the model to delete')

    def handle(self, *args, **kwargs):
        app_label = kwargs['app_label']
        model_name = kwargs['model_name']

        try:
            model = apps.get_model(app_label, model_name)
        except LookupError:
            raise CommandError(f"Model '{app_label}.{model_name}' not found.")

        model.objects.all().delete()

        if 'sqlite' in settings.DATABASES['default']['ENGINE']:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{model._meta.db_table}';")
        elif 'postgresql' in settings.DATABASES['default']['ENGINE']:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT setval(pg_get_serial_sequence('{model._meta.db_table}', 'id'), 1, false);")

        self.stdout.write(self.style.SUCCESS(f'All data from {app_label}.{model_name} has been deleted and ID sequence reset'))