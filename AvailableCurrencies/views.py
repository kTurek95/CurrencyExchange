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
from django.contrib.auth.decorators import login_required
from .models import AvailableCurrency, CurrencyExchangeRate
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
    paginator = Paginator(available_currencies, 30)
    page_number = request.GET.get('page')
    available_currencies_list = paginator.get_page(page_number)
    context = {
        'currencies_list': available_currencies_list,
        'active_menu': 'Available currencies'}
    return render(request, 'AvailableCurrencies/currencies_list.html', context)


@ login_required()
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


@login_required()
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
    Generates interesting and concise facts about a set of chosen currencies using an AI model.
    This function first calls 'get_currency_from_database' to retrieve a list of currencies.
    It then creates a request for the OpenAI GPT-4 model, asking it to generate facts about these currencies.
    The AI's response is formatted and split into separate facts corresponding to each currency.
    Finally, these facts are paired with their respective currencies and passed to the template
    'currency-news.html' for rendering.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: An HttpResponse object that renders the 'currency-news.html' template,
                      including the list of currencies paired with their AI-generated facts.
    """
    chosen_currencies_list = get_currency_from_database()
    client = OpenAI()
    responses_currencies_list = []
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "Hey Currency assistance, you're a specialist in currency and cryptocurrencies."
                           "I want you to write me an interesting fact about the currencies I provide you with."
                           "The facts should be short and concise."
                           "They don't have to strictly relate to the  specific  currency;"
                           "they  can  be  tangential  topics.Please write st least 2 sentences about each currency. "
                           "Here  's the example structure I' m  expecting:"
                           f"{chosen_currencies_list[0]}: "
                           f"{chosen_currencies_list[1]}:  "
                           f"{chosen_currencies_list[2]} :"
            },
            {
                "role": "user",
                "content": f"Hey chat, can you please write down some fun facts about {chosen_currencies_list} ?"
                           f"Please write only responses without any unnecessary text."
            }
        ],
        temperature=1,
        max_tokens=700,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    responses_currencies_list.append(response.choices[0].message.content)
    responses_string = responses_currencies_list[0]
    responses = responses_string.split("\n\n")
    currency_and_responses = zip(chosen_currencies_list, responses)
    currency_and_responses_list = list(currency_and_responses)

    context = {
        'currency_and_responses_list': currency_and_responses_list
    }

    return render(request, 'AvailableCurrencies/currency-news.html', context)
