import json
import os
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from AvailableCurrencies.models import AvailableCurrency, CurrencyExchangeRate


def currency_view(request):
    """
    Renders the currency overview page with details for each available currency.

    This function retrieves a list of all available currencies, fetches the latest
    exchange rate for each currency to USD, and gathers images from the specified directory.
    It prepares this data in a context dictionary and renders the 'about.html' template.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A response that renders the 'about.html' template with the following context:
            - 'currency_view':
             A queryset of all available currencies, ordered by their code.
            - 'latest_currency_rates':
             A JSON-encoded list containing the latest exchange rate for each currency.
            - 'photos':
             A list of filenames from the 'main/static/main/img' directory,
              representing images for each currency.
            - 'active_menu':
             A string indicating the currently active menu (in this case, 'Home').
    """
    photos_dir = os.listdir('main/static/main/img')
    currency = AvailableCurrency.objects.all().order_by('code')

    # Fetching the latest exchange rate for each currency
    latest_currency_rates = (
        CurrencyExchangeRate.objects.values
        ('currency__code').annotate(latest_rate=Max('rate_to_usd')))
    latest_currency_rates_list = list(latest_currency_rates.values('currency__code', 'latest_rate'))
    latest_currency_rates_list_json = json.dumps(latest_currency_rates_list)

    context = {
        'currency_view': currency,
        'latest_currency_rates': latest_currency_rates_list_json,
        'photos': photos_dir,
        'active_menu': 'Home'
    }
    return render(request, 'main/about.html', context)


def calculate(request):
    """
    Handles the calculation of the exchange rate from a selected currency to USD.

    This function processes a POST request containing the selected currency and the amount.
    It retrieves the exchange rate for the selected currency to USD from the database,
    inverts the rate (since the stored rate is USD to the selected currency), and calculates
    the equivalent amount in USD.

    Args:
        request (HttpRequest): The HTTP request object containing POST data with the selected
                               currency ('currency') and amount ('amount').

    Returns:
        JsonResponse: A JSON response containing the following data:
            - 'result': The calculated amount in USD.
            - 'currency_name': The name of the selected currency.
            - 'rate': The exchange rate from the selected currency to USD.

        If the request method is not POST or if there's an error in the request, a JSON response
        with an error message and a 400 status code is returned.
    """
    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        amount = float(request.POST.get('amount'))

        currency_instance = AvailableCurrency.objects.get(code=selected_currency)
        currency_name = currency_instance.name

        rate = CurrencyExchangeRate.objects.filter(currency__code=selected_currency).first()
        # calculate currency rate to usd
        proper_rate = 1 / float(rate.rate_to_usd)
        result = round(proper_rate * amount, 2)

        return JsonResponse({
            'result': result,
            'currency_name': currency_name,
            'rate': round(proper_rate, 2) if rate else None
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
