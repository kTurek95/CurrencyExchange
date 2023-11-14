from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
import json
import requests
from .models import AvailableCurrency, CurrencyExchangeRate


def currencies(request):
    return HttpResponse('Lista dostępnych Walut')


def currencies_list(request):
    currencies = AvailableCurrency.objects.all().order_by('name')
    paginator = Paginator(currencies, 30)
    page_number = request.GET.get('page')
    currencies_list = paginator.get_page(page_number)
    context = {'currencies_list': currencies_list}
    return render(request, 'AvailableCurrencies/currencies_list.html', context)


def get_currencies_symbol_from_api(request):
    params = {
        'apikey': 'e0ad4966bceb4346b7949c5e3d5a6dee',
    }
    r = requests.get('https://api.currencyfreaks.com/v2.0/supported-currencies', params)

    try:
        content = r.json()
    except json.JSONDecodeError:
        return HttpResponse('Wrong format')
    else:
        for currency_key in content["supportedCurrenciesMap"]:
            currency_data = content["supportedCurrenciesMap"][currency_key]

            status_bool = currency_data['status'] == 'AVAILABLE'

            AvailableCurrency.objects.update_or_create(
                code=currency_data['currencyCode'],
                defaults={
                    'name': currency_data['currencyName'],
                    'country_code': currency_data.get('countryCode', ''),
                    'country_name': currency_data.get('countryName', ''),
                    'status': status_bool,
                }
            )


def currencies_details(request, currency_id: int):
    currency = AvailableCurrency.objects.get(pk=currency_id)
    rate = CurrencyExchangeRate.objects.filter(currency=currency).first()
    context = {'currency_details': currency,
               'rates': rate}
    return render(request, 'AvailableCurrencies/currencies_details.html', context)


def currencies_rate(request):
    rate = CurrencyExchangeRate.objects.all().order_by('currency__code')
    paginator = Paginator(rate,30)
    page_number = request.GET.get('page')
    rates_list = paginator.get_page(page_number)
    context = {'currencies_rate': rates_list}
    return render(request, 'AvailableCurrencies/currencies_rate.html', context)
