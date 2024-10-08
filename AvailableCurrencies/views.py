"""
This module provides views for handling currency-related data in a Django application.
It includes functionalities to display available
currencies, currency rates, historical currency rates with graphical representation,
and comparison of currency rates from the previous day.

Functions:
    currencies - Returns a list of available currencies.
    currencies_list - Displays a paginated list of available currencies.
    currencies_details - Shows details and historical rate chart for a selected currency.
    currencies_rate - Displays current rates for different currencies.
    compare_previous_day_rate - Compares currency rates with the previous day's rates.
"""

from datetime import datetime, timedelta, date
import random

import matplotlib
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Max
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import AvailableCurrency, CurrencyExchangeRate, CurrencyNews
from openai import OpenAI


def currencies():
    """
    Returns a HttpResponse with a list of available currencies.
    """
    return HttpResponse('Available currencies list')


def currencies_list(request):
    """
    Displays a paginated list of available currencies.

    Args:
        request: HttpRequest object used to generate the currencies list.

    Returns:
        HttpResponse with a rendered template containing the list of currencies.
    """
    available_currencies = (
        AvailableCurrency.objects.exclude(Q(country_name='Global')).order_by('name'))
    paginator = Paginator(available_currencies, 12)
    page_number = request.GET.get('page')
    available_currencies_list = paginator.get_page(page_number)
    context = {
        'currencies_list': available_currencies_list,
        'active_menu': 'Available currencies'}
    return render(request, 'AvailableCurrencies/currencies_list.html', context)


def currencies_details(request, currency_id: int):
    """
    Displays the details and historical exchange rate chart for a selected currency.

    Args:
        request: HttpRequest object used to generate the details.
        currency_id (int): The ID of the currency for which details are to be displayed.

    Returns:
        HttpResponse with a rendered template containing currency details and a chart.
    """
    matplotlib.use('Agg')
    five_days_ago = datetime.now() - timedelta(days=5)

    dates = []
    currency_rates = []

    currency = AvailableCurrency.objects.get(pk=currency_id)
    rate = CurrencyExchangeRate.objects.filter(currency=currency).first()

    available_currencies = AvailableCurrency.objects.filter(id=currency_id)
    rates = CurrencyExchangeRate.objects.filter(
        currency_id=available_currencies.first(),
        api_date_updated__gt=five_days_ago
    )
    for rate in rates:
        dates.append(rate.api_date_updated)
        currency_rates.append(rate.rate_to_usd)

    data_pairs = sorted(zip(dates, currency_rates), key=lambda x: x[1])
    sorted_dates, sorted_currency_rates = zip(*data_pairs)

    sorted_dates = \
        [datetime.strptime
         (date, '%Y-%m-%d') if isinstance(date, str)
         else date for date in sorted_dates]
    sorted_currency_rates = [float(rate) for rate in sorted_currency_rates]

    plt.figure(figsize=(10, 5))

    plt.bar(sorted_dates, sorted_currency_rates)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.ylim(min(sorted_currency_rates) - 1, max(sorted_currency_rates) + 1)

    plt.title(available_currencies.first())
    plt.xlabel('Dates')
    plt.ylabel('Currency rates')

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.grid(True)

    image_path = f'AvailableCurrencies/static/AvailableCurrencies/img/chart_{currency_id}.png'
    plt.savefig(image_path)
    plt.close()

    context = {'currency_details': currency,
               'rates': rate,
               'image_name': f'chart_{currency_id}.png',
               'active_menu': 'Available currencies'
               }

    return render(request, 'AvailableCurrencies/currencies_details.html', context)


def currencies_rate(request):
    """
    Displays a page with current exchange rates of currencies.

    Args:
       request: HttpRequest object used to generate the list of currency rates.

    Returns:
       HttpResponse with a rendered template containing the current rates of currencies.
    """
    latest_rates = (
        CurrencyExchangeRate.objects.values
        ('currency_id').annotate(latest_date=Max('api_date_updated')))
    rate = (CurrencyExchangeRate.objects.filter(
        api_date_updated__in=[item['latest_date'] for item in latest_rates]
    ).order_by('currency__code').select_related('currency').order_by('currency__code')
            .exclude(Q(currency__country_name='Global')))
    paginator = Paginator(rate, 15)
    page_number = request.GET.get('page')
    rates_list = paginator.get_page(page_number)
    context = {
        'currencies_rate': rates_list,
        'active_menu': 'Currencies rate'}
    return render(request, 'AvailableCurrencies/currencies_rate.html', context)


def compare_previous_day_rate(request):
    """
    Compares the exchange rates of currencies with those of the previous day.

    Args:
        request: HttpRequest object used to generate comparative data.

    Returns:
        HttpResponse with a rendered template
        containing the comparison of currency rates from the previous day.
    """
    today = date.today()
    currency_list = AvailableCurrency.objects.all()
    yesterday_date = today - timedelta(days=1)
    today_rates = \
        {rate.currency_id:
             rate for rate in CurrencyExchangeRate.objects.filter(api_date_updated=today)}
    yesterday_rates = {rate.currency_id: rate for rate in
                       CurrencyExchangeRate.objects.filter(api_date_updated=yesterday_date)}
    difference = []
    for currency in currency_list:
        today_rate = today_rates.get(currency.id)
        yesterday_rate = yesterday_rates.get(currency.id)

        if today_rate and yesterday_rate:
            diff = round(float(today_rate.rate_to_usd) - float(yesterday_rate.rate_to_usd), 6)
            difference.append((currency, diff))

    context = {
        'difference': difference,
        'active_menu': 'Available currencies'}

    return render(request, 'AvailableCurrencies/currency-compare-to-previous-day.html', context)


def get_currency_from_database():
    """
    Retrieves a random selection of four available currencies from the database,
    excluding any currency labeled as 'Global'. This function queries the AvailableCurrency
    model, fetches all currency records except for those associated with 'Global',
    and then randomly selects four distinct currencies from this filtered list.

    Returns:
        list: A list of four randomly chosen currency objects.
    """
    currency = AvailableCurrency.objects.all().exclude(country_name='Global')
    chosen_currency = random.choices(currency, k=4)
    return chosen_currency


def chosen_currency_news(request):
    """
    Displays the latest currency news on the website.

    The function retrieves the last 4 records from the `CurrencyNews` model based on the `id` field (in descending order) and processes them to extract the currency code and the associated fact or news. The results are then passed to the `currency-news.html` template, where they are displayed as a list of paired values (currency code, fact).

    Args:
        request: An `HttpRequest` object representing the HTTP request sent by the user.

    Returns:
        HttpResponse: An `HttpResponse` object containing the generated HTML page with currency news.
    """
    currency_news_from_database = CurrencyNews.objects.order_by('-id')[:4]
    currency_code_and_name = []
    currency_fun_fact = []
    for currency_news in currency_news_from_database:
        currency_code_and_name.append(str(currency_news).split(':')[0])
        currency_fun_fact.append(str(currency_news).split(':')[1])

    currency_news_zip = zip(currency_code_and_name, currency_fun_fact)

    context = {
        'currency_news_zip': list(currency_news_zip)
    }

    return render(request, 'AvailableCurrencies/currency-news.html', context)
