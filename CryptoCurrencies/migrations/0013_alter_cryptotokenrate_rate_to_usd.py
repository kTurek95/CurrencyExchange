# Generated by Django 4.2.7 on 2024-02-15 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCurrencies', '0012_alter_cryptotokenrate_rate_to_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptotokenrate',
            name='rate_to_usd',
            field=models.CharField(max_length=20),
        ),
    ]
