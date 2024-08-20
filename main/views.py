from django.http import JsonResponse
from django.shortcuts import render
from AvailableCurrencies.models import AvailableCurrency, CurrencyExchangeRate


def currency_view(request):
    currency = AvailableCurrency.objects.all().order_by('code')
    context = {
        'currency_view': currency,
        'active_menu': 'Home'
    }
    return render(request, 'main/about.html', context)


def calculate(request):
    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        amount = float(request.POST.get('amount'))

        currency_instance = AvailableCurrency.objects.get(code=selected_currency)
        currency_name = currency_instance.name

        rate = CurrencyExchangeRate.objects.filter(currency__code=selected_currency).first()
        result = round(float(rate.rate_to_usd) * amount, 2)

        return JsonResponse({
            'result': result,
            'currency_name': currency_name,
            'rate': round(float(rate.rate_to_usd), 2) if rate else None
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)