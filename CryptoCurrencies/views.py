from django.shortcuts import render
from django.core.paginator import Paginator
from .models import CryptoTokenCurrency
from django.contrib.auth.decorators import login_required


def crypto_token(request):
    crypto = CryptoTokenCurrency.objects.all().order_by('code')
    paginator = Paginator(crypto, 300)
    page_number = request.GET.get('page')
    crypto_token = paginator.get_page(page_number)
    context = {'crypto_token': crypto_token}
    return render(request, 'CryptoCurrencies/crypto-token-list.html', context)


@ login_required
def crypto_token_details(request, crypto_id: int):
    crypto_details = CryptoTokenCurrency.objects.get(pk=crypto_id)
    context = {'crypto_token_details': crypto_details}

    return render(request, 'CryptoCurrencies/crypto-token-details.html', context)