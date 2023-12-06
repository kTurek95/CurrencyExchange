from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from .models import CryptoTokenCurrency


def crypto_token(request):
    crypto = CryptoTokenCurrency.objects.all()
    paginator = Paginator(crypto, 400)
    page_number = request.GET.get('page')
    crypto_token = paginator.get_page(page_number)
    context = {'crypto_token': crypto_token}
    return render(request, 'CryptoCurrencies/crypto-token-list.html', context)