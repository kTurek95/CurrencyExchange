from django.shortcuts import render
from wallet.forms import WalletTransactionForm, SubmitWalletTransactionForm
from .models import Wallet, Transaction
from django.contrib import messages
from AvailableCurrencies.models import AvailableCurrency, CurrencyExchangeRate
from CryptoCurrencies.models import CryptoTokenCurrency, CryptoTokenRate
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal


def wallet(request):
    """
   Handle the wallet creation and display available currencies and crypto tokens.

   This view allows the user to create a new wallet for either standard currencies or
   crypto tokens. It limits the user to have only one wallet of each type and a total of
   two wallets. If the user attempts to create more than the allowed number of wallets,
   or an additional wallet of the same type, an error message is displayed.

   Args:
   - request (HttpRequest): The HTTP request object containing user data and method type.

   Returns:
   - HttpResponse: Renders the wallet creation page with a list of available currencies
     and crypto tokens, or a wallet created confirmation page.
   """
    currencies = AvailableCurrency.objects.all()
    crypto_currencies = CryptoTokenCurrency.objects.all()

    if request.method == 'POST':
        wallet_types = ['Currency', 'Crypto']
        wallet_type = request.POST.get('wallet_type')
        wallet_count = Wallet.objects.filter(user=request.user).count()
        if wallet_type in wallet_types:
            if wallet_count < 2:
                if wallet_type == 'Currency':
                    currency_id = request.POST.get('currency')
                    if not Wallet.objects.filter(user=request.user, currency_id__isnull=False).exists():
                        Wallet.objects.create(
                            user_id=request.user.id,
                            balance=100.00,
                            currency_id=currency_id
                        )
                        return render(request, 'wallet/wallet_created.html')
                    else:
                        messages.error(request, 'You can have only 1 currency wallet')
                elif wallet_type == 'Crypto':
                    crypto_currency_id = request.POST.get('crypto_currency')
                    if not Wallet.objects.filter(user=request.user, crypto_currency_id__isnull=False).exists():
                        Wallet.objects.create(
                            user_id=request.user.id,
                            balance=100.00,
                            crypto_currency_id=crypto_currency_id
                        )
                        return render(request, 'wallet/wallet_created.html')
                    else:
                        messages.error(request, 'You can have only 1 cryptocurrency wallet')
            else:
                messages.error(request, 'You can have only 2 wallets')
        else:
            messages.error(request, 'Please choose wallet type')

    return render(request, 'wallet/wallet.html', {
        'currencies': currencies,
        'crypto_currencies': crypto_currencies
    })


def wallet_balance(request):
    """
    Display the balance of wallets for the authenticated user.

    This view fetches and displays the balance of all wallets associated with the
    authenticated user. If the user is not authenticated, the view does not display
    any wallet information.

    Args:
    - request (HttpRequest): The HTTP request object containing user data.

    Returns:
    - HttpResponse: Renders the account balance page, showing the balance of each wallet
      for the authenticated user.
    """
    currency_amount = None
    crypto_amount = None
    if request.user.is_authenticated:
        user_id = request.user.id
        accounts = Wallet.objects.filter(user_id=user_id)
        for account in accounts:
            if account.currency_id is not None:
                account_currency_id = account.currency_id

                # przeliczenie wartości portfela na USD
                chosen_currency_rate = CurrencyExchangeRate.objects.filter(currency_id=account_currency_id).order_by(
                    'api_date_updated').first()
                currency_rate_in_usd = str(chosen_currency_rate).split('-')[-1].lstrip()
                currency_amount = "{:.2f}".format(float(currency_rate_in_usd) * float(account.balance))

            elif account.crypto_currency_id is not None:
                account_crypto_currency_id = account.crypto_currency_id

                # przeliczenie wartości portfela na USD
                chosen_crypto_rate = CryptoTokenRate.objects.filter(token_id=account_crypto_currency_id).order_by(
                    '-date').first()
                crypto_rate_in_usd = str(chosen_crypto_rate).split(':')[-1].lstrip()
                crypto_amount = "{:.2f}".format(float(crypto_rate_in_usd) * float(account.balance))

    return render(request, 'wallet/account_balance.html', {
        'accounts': accounts,
        'currency_amount': currency_amount,
        'crypto_amount': crypto_amount
    })


def wallet_selection(request):
    """
    This view function handles different wallet-related actions for authenticated users. It retrieves
    and displays the user's wallets, and based on the request method (GET or POST), it either displays
    wallet information or processes wallet transactions.

    For GET requests, the function simply returns the user's wallets.

    For POST requests, it processes two types of actions:
    - 'show_transaction': Displays transactions for a selected wallet. The transaction display
      varies based on whether the wallet is a currency wallet or a crypto wallet.
    - 'make_transaction': Redirects to a page for making transactions.

    Args:
    - request: HttpRequest object containing metadata and information about the request
      (such as the method type, POST data, and session information).

    Returns:
    - HttpResponse: Renders the appropriate template with context data based on the user's
      request and actions. Possible templates rendered are:
        - 'wallet/currency_history.html' for showing currency wallet transactions.
        - 'wallet/crypto_history.html' for showing crypto wallet transactions.
        - 'wallet/wallet_selection.html' for selecting a wallet or showing errors.

    Raises:
    - ValidationError: If a non-integer wallet ID is selected.
    - Any database-related exceptions if the wallet or transaction objects cannot be retrieved.
    """
    context = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        user_wallets = Wallet.objects.filter(user_id=user_id)
        context['user_wallets'] = user_wallets

        if request.method == "POST":
            action = request.POST.get('action')
            selected_wallet_id = request.POST.get('selected_wallet')
            request.session['selected_wallet_id'] = selected_wallet_id
            if selected_wallet_id.isdigit():
                if action == 'show_transaction':
                    selected_wallet = Wallet.objects.get(id=selected_wallet_id)
                    transactions = Transaction.objects.filter(wallet=selected_wallet)
                    context['transactions'] = transactions
                    if selected_wallet.currency:
                        return render(request, 'wallet/currency_history.html', context)
                    elif selected_wallet.crypto_currency:
                        return render(request, 'wallet/crypto_history.html', context)
                    else:
                        messages.error(request, 'Please choose a wallet type')
                elif action == 'make_transaction':
                    return HttpResponseRedirect(reverse('wallet:transaction'))
            else:
                context['error'] = 'Please select a valid wallet.'

        return render(request, 'wallet/wallet_selection.html', context)


def wallet_transaction(request):
    """
    [In Progress] Prepares the interface for conducting transactions.

    This view is intended to render a page where users will be able to carry out
    transactions. Currently, the page is in the development phase and does not yet
    include the logic for processing transactions.

    Args:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: Renders the page for making transactions.
    """
    return render(request, 'wallet/make_transaction.html')