from django.shortcuts import render
from AvailableCurrencies.models import AvailableCurrency, CurrencyExchangeRate


def currency_view(request):
    result = None
    currency = AvailableCurrency.objects.all().order_by('code')
    rate = None
    
    if request.method == 'POST':
        selected_currency = request.POST.get('currency')
        amount = float(request.POST.get('amount'))
        
        rate = CurrencyExchangeRate.objects.filter(currency__code=selected_currency).first()
        result = round(float(rate.rate_to_usd) * amount, 2)

    context = {
        'currency_view': currency,
        'result': result,
        'currency_rate': round(float(rate.rate_to_usd), 2) if rate else None
    }
    return render(request, 'main/about.html', context)
