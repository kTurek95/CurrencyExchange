# Generated by Django 4.2.7 on 2023-12-02 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCurrencies', '0003_cryptotokenrate'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptotokenrate',
            name='rate_to_usd',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
