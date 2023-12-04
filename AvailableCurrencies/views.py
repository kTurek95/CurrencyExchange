from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as mdates
from .models import AvailableCurrency, CurrencyExchangeRate


def currencies(request):
    return HttpResponse('Lista dostępnych Walut')


def currencies_list(request):
    currencies = AvailableCurrency.objects.exclude(Q(country_name='Global'))
    paginator = Paginator(currencies, 30)
    page_number = request.GET.get('page')
    currencies_list = paginator.get_page(page_number)
    context = {'currencies_list': currencies_list}
    return render(request, 'AvailableCurrencies/currencies_list.html', context)


def currencies_details(request, currency_id: int):
    matplotlib.use('Agg')
    five_days_ago = datetime.now() - timedelta(days=5)

    dates = []
    currency_rates = []

    currency = AvailableCurrency.objects.get(pk=currency_id)
    rate = CurrencyExchangeRate.objects.filter(currency=currency).first()

    currencies = AvailableCurrency.objects.filter(id=currency_id)
    rates = CurrencyExchangeRate.objects.filter(
        currency_id=currencies.first(),
        api_date_updated__gt=five_days_ago
    )
    for rate in rates:
        dates.append(rate.api_date_updated)
        currency_rates.append(rate.rate_to_usd)

    data_pairs = sorted(zip(dates, currency_rates), key=lambda x: x[1])
    sorted_dates, sorted_currency_rates = zip(*data_pairs)

    sorted_dates = [datetime.strptime(date, '%Y-%m-%d') if isinstance(date, str) else date for date in sorted_dates]
    sorted_currency_rates = [float(rate) for rate in sorted_currency_rates]

    plt.figure(figsize=(10, 5))

    plt.bar(sorted_dates, sorted_currency_rates)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())

    plt.ylim(min(sorted_currency_rates) - 1, max(sorted_currency_rates) + 1)

    plt.title(currencies.first())
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
               'image_name': f'chart_{currency_id}.png'
               }

    return render(request, 'AvailableCurrencies/currencies_details.html', context)


def currencies_rate(request):
    latest_rates = CurrencyExchangeRate.objects.values('currency_id').annotate(latest_date=Max('api_date_updated'))
    rate = CurrencyExchangeRate.objects.filter(
        api_date_updated__in=[item['latest_date'] for item in latest_rates]
    ).order_by('currency__code').select_related('currency').order_by('currency__code')
    paginator = Paginator(rate, 30)
    page_number = request.GET.get('page')
    rates_list = paginator.get_page(page_number)
    context = {'currencies_rate': rates_list}
    return render(request, 'AvailableCurrencies/currencies_rate.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('main:hello'))
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})
