# Generated by Django 4.2.7 on 2023-11-09 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AvailableCurrencies', '0005_alter_availablecurrency_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='availablecurrency',
            name='country_code',
            field=models.CharField(max_length=5, null=True),
        ),
    ]