# Generated by Django 4.2.7 on 2024-02-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCurrencies', '0005_alter_cryptotokenrate_rate_to_usd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptotokencurrency',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
