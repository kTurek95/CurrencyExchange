# Generated by Django 4.2.7 on 2024-02-15 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CryptoCurrencies', '0010_alter_cryptotokencurrency_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptotokencurrency',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
