from django.shortcuts import render
from django.http import HttpResponse
from .models import CurrencyPair


def currency_pairs(request):
    return HttpResponse('Lista dostępnych par walutowych')


def pairs_list(request):
    pair = CurrencyPair.objects.all()
    context = {'pairs_list': pair}
    return render(request, 'CurrencyPairs/pairs_list.html', context)