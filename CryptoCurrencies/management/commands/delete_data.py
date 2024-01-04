from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Cleans a specified database table'

    def add_arguments(self, parser):
        parser.add_argument('table_name', type=str, help='Name of the table to delete')

    def handle(self, *args, **kwargs):
        table_name = kwargs['table_name']

        table_name.objects.all().delete()

        self.stdout.write('All data has been deleted')