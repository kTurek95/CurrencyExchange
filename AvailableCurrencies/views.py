from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .models import AvailableCurrency


def currencies(request):
    return HttpResponse('Lista dostępnych Walut')


def currencies_list(request):
    currencies = AvailableCurrency.objects.all()
    context = {'currencies_list': currencies}
    return render(request, 'AvailableCurrencies/currencies_list.html', context)