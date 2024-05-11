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


def prepare_and_process_wallet_transaction(request):
    """
    Prepares and processes a wallet transaction for an authenticated user based on session data and form inputs.
    This function determines whether the user's wallet uses traditional currency or cryptocurrency and
    prepares the appropriate form for transaction input. If the request method is POST, the function will
    attempt to process the transaction.

    Args:
        request (HttpRequest): The HTTP request object containing user and session data.

    Returns:
        HttpResponse: Renders the transaction form with the relevant context or redirects after processing the transaction.

    Raises:
        ValueError: If the user is unauthenticated or if the form input is invalid, an error message is displayed.
    """

    wallet_instance = None
    selected_wallet_id = request.session.get('selected_wallet_id')
    if request.user.is_authenticated:
        user_id = request.user.id
        wallet_instance = Wallet.objects.get(user_id=user_id, id=selected_wallet_id)

        if wallet_instance.currency_id is None and wallet_instance.crypto_currency_id is not None:
            wallet_info = f'{wallet_instance.balance} - {wallet_instance.crypto_currency.name}'
            crypto = CryptoTokenCurrency.objects.all()
            form = WalletTransactionForm(currency_choices=crypto)

        elif wallet_instance.currency_id is not None and wallet_instance.crypto_currency_id is None:
            wallet_info = f'{wallet_instance.balance} - {wallet_instance.currency.name}'
            currrencies = AvailableCurrency.objects.all().exclude(country_name='Global').order_by('code')
            form = WalletTransactionForm(currency_choices=currrencies)

    if request.method == 'POST':
        if wallet_instance.currency_id is not None and wallet_instance.crypto_currency_id is None:
            form = (
                WalletTransactionForm(
                    request.POST, currency_choices=AvailableCurrency.objects.all().exclude(
                        country_name='Global').order_by('code')))
        elif wallet_instance.currency_id is None and wallet_instance.crypto_currency_id is not None:
            form = WalletTransactionForm(request.POST, currency_choices=None)

        if form.is_valid():
            wallet_instance_id = wallet_instance.id
            request.session['wallet_instance_id'] = wallet_instance_id
            amount = form.cleaned_data['amount']
            request.session['amount'] = int(amount)
            if 'dane_formularza_crypto' in request.session:
                del request.session['dane_formularza_crypto']
            elif 'dane_formularza_currency' in request.session:
                del request.session['dane_formularza_currency']

            if 'currency' in form.cleaned_data.keys():
                selected_currency = form.cleaned_data['currency'].name
                request.session['selected_currency'] = selected_currency
                currency_id = form.cleaned_data['currency'].id
                request.session['dane_formularza_currency'] = currency_id

            elif 'crypto_currency' in form.cleaned_data.keys():
                selected_crypto = form.cleaned_data['crypto_currency'].name
                request.session['selected_crypto'] = selected_crypto
                crypto_currency_id = form.cleaned_data['crypto_currency'].id
                request.session['dane_formularza_crypto'] = crypto_currency_id

            return HttpResponseRedirect(reverse('wallet:wallet_transaction'))

        else:
            messages.error(request, 'Invalid input.')

    else:
        if wallet_instance.currency_id is not None and wallet_instance.crypto_currency_id is None:
            form = (
                WalletTransactionForm(
                    currency_choices=AvailableCurrency.objects.all().exclude(
                        country_name='Global').order_by('code')))
        elif wallet_instance.currency_id is None and wallet_instance.crypto_currency_id is not None:
            form = (
                WalletTransactionForm(currency_choices=None))

    context = {
        'wallet_info': wallet_info,
        'form': form,
    }
    return render(request, 'wallet/make_transaction.html', context)


def wallet_transaction(request):
    """
    Handles the transaction processes within a user's wallet, supporting both cryptocurrency and standard currency transactions based on the user's selection. The function determines the type of wallet (crypto or currency), fetches the latest exchange rate for the selected type, calculates transaction values in both the wallet's currency and USD, and updates the wallet balance if the transaction is approved.

    Parameters:
    - request (HttpRequest): The HTTP request object containing session data like selected currency, transaction amount, and other necessary information.

    Returns:
    - HttpResponse: Renders the 'transaction finalization.html' template with the context containing transaction details and updates based on the outcome (success or error).

    The function also handles form initialization and submission, updates the wallet's balance upon successful transactions, and logs transaction details. If a user is authenticated and the POST method is used, the function attempts to perform the transaction and update the database accordingly. It provides feedback to the user via messages indicating the success or failure of the transaction.
    """

    wallet_instance_id = request.session.get('wallet_instance_id')
    wallet_instance = Wallet.objects.get(id=wallet_instance_id)

    if str(wallet_instance) == 'Crypto wallet':
        crypto = request.session.get('selected_crypto')
        current_wallet_crypto_id = CryptoTokenCurrency.objects.get(id=wallet_instance.crypto_currency_id).id

        current_wallet_crypto_id_rate = (
            CryptoTokenRate.objects.filter(
                token_id=current_wallet_crypto_id).order_by('-date').first())

        current_wallet_crypto_id_rate_format = str(current_wallet_crypto_id_rate).split(':')[-1].lstrip()

    elif str(wallet_instance) == 'Currency wallet':
        currency = request.session.get('selected_currency')
        current_wallet_currency_id = (
            AvailableCurrency.objects.get(
                code=str(wallet_instance.currency).split('-')[0].rstrip()))

        current_wallet_currency_id_rate = (
            CurrencyExchangeRate.objects.filter(
                currency_id=current_wallet_currency_id).order_by('api_date_updated').first())

        current_wallet_currency_id_rate_format = str(current_wallet_currency_id_rate).split("-")[-1].lstrip()

    wallet_instance_currency_id = Wallet.objects.get(id=wallet_instance_id).currency_id
    wallet_instance_crypto_currency_id = Wallet.objects.get(id=wallet_instance_id).crypto_currency_id

    currency_wallet_instance_balance = Wallet.objects.get(id=wallet_instance_id).balance
    crypto_wallet_instance_balance = Wallet.objects.get(id=wallet_instance_id).balance

    currency_rate = None
    crypto_rate = None
    total_crypto_transaction_value_in_usd = None
    total_currency_transaction_value_in_usd = None
    dane_formularza_currency = request.session.get('currency_form_data')
    dane_formularza_crypto = request.session.get('crypto_form_data')
    amount = request.session.get('amount')

    # jeśli użytkownik wybierze zwykłą walutę
    # if the user selects a regular currency
    if dane_formularza_currency is not None:
        # pobranie informacji na temat waluty w portfelu i przeliczenie jej wartosci na usd
        # retrieve information about the wallet's currency and convert its value to USD
        currency_rate_from_database = (
            CurrencyExchangeRate.objects.filter(
                currency_id=wallet_instance_currency_id).order_by('api_date_updated').first().rate_to_usd)
        currency_wallet_balance_in_usd = (
            "{:.2f}".format(float(currency_rate_from_database) * float(currency_wallet_instance_balance)))

        # obliczenie całkowitej sumy transakcji w usd
        # calculate the total transaction amount in USD
        currency_rate = (
            CurrencyExchangeRate.objects.filter
            (currency_id=dane_formularza_currency).order_by('api_date_updated').first()).rate_to_usd
        currency_rate_value_to_usd = "{:.2f}".format(1 / float(currency_rate))
        total_currency_transaction_value_in_usd = "{:.2f}".format(amount * float(currency_rate_value_to_usd))

        # obliczenie sumy transakcji w walucie portfela
        # calculate the transaction amount in the wallet's currency
        transaction_amount_in_currency_wallet = "{:.2f}".format(
            float(total_currency_transaction_value_in_usd) / float(current_wallet_currency_id_rate_format)\
        )

        # dane do formularza
        # data for the form
        initial_data = {
            'wallet_balance': wallet_instance.balance,
            'wallet_balance_in_usd': currency_wallet_balance_in_usd,
            'selected_currency': currency,
            'currency_amount': amount,
            'currency_rate': currency_rate_value_to_usd,
            'transaction_sum_in_usd': total_currency_transaction_value_in_usd,
            'transaction_sum': transaction_amount_in_currency_wallet
        }

        balance_after_transaction = (
            "{:.2f}".format(
                float(currency_wallet_balance_in_usd) - float(total_currency_transaction_value_in_usd), 2))
        form = SubmitWalletTransactionForm(initial=initial_data)

        if request.method == 'POST' and request.user.is_authenticated:
            if float(currency_wallet_balance_in_usd) >= float(total_currency_transaction_value_in_usd):
                # wartość transakcji w walucie portfela (typ decimal)
                # transaction value in the wallet's currency (decimal type)

                decimal_value = "{:.2f}".format(Decimal(transaction_amount_in_currency_wallet))
                wallet_instance.balance -= Decimal(decimal_value)
                wallet_instance.save()

                # tworzenie transakcji
                # creating the transaction
                new_transaction = Transaction(
                    user_id=request.user,
                    wallet=wallet_instance,
                    amount=amount,
                    transaction_type=Transaction.BUY,
                    purchased_currency=currency,
                    status=Transaction.COMPLETED,
                    date=timezone.now(),
                    value_in_USD=total_currency_transaction_value_in_usd,
                    balance_after_transaction=balance_after_transaction
                )

                new_transaction.save()
                messages.success(request, 'The transaction was successful')
                return HttpResponseRedirect(reverse('main:currency'))
            else:
                new_transaction = Transaction(
                    wallet=wallet_instance,
                    amount=amount,
                    transaction_type=Transaction.BUY,
                    purchased_currency=currency,
                    status=Transaction.REJECTED,
                    date=timezone.now(),
                    value_in_USD=total_currency_transaction_value_in_usd,
                    balance_after_transaction=currency_wallet_balance_in_usd
                )
                new_transaction.save()
                messages.error(request, 'You do not have sufficient funds in your account')

    # jeśli użytkownik wybierze kryptowalutę
    # if the user selects a cryptocurrency
    elif dane_formularza_crypto is not None:

        # pobranie kursu kryptowaluty w portfelu z bazy danych
        # retrieve the cryptocurrency rate from the database for the wallet
        crypto_rate_from_database =\
            CryptoTokenRate.objects.filter(
                token_id=wallet_instance_crypto_currency_id).order_by('-date').first().rate_to_usd

        # zamiana waluty portfela na usd
        # convert the wallet's currency to USD
        crypto_wallet_balance_in_usd = (
            "{:.2f}".format(float(crypto_rate_from_database) * float(crypto_wallet_instance_balance)))

        # obliczenie całkowitej sumy transakcji w usd
        # calculate the total transaction amount in USD
        crypto_rate = (
            CryptoTokenRate.objects.filter
            (token_id=dane_formularza_crypto).order_by('-date').first()).rate_to_usd
        total_crypto_transaction_value_in_usd = "{:.2f}".format(amount * float(crypto_rate))

        # obliczenie sumy transakcji w walucie portfela
        # calculate the transaction amount in the wallet's currency
        transaction_amount_in_crypto_wallet = "{:.2f}".format(
            float(total_crypto_transaction_value_in_usd) / float(current_wallet_crypto_id_rate_format)
        )

        # dane do formularza
        # data for the form
        initial_data = {
            'wallet_balance': wallet_instance.balance,
            'wallet_balance_in_usd': crypto_wallet_balance_in_usd,
            'selected_currency': crypto,
            'currency_amount': amount,
            'currency_rate': crypto_rate,
            'transaction_sum_in_usd': total_crypto_transaction_value_in_usd,
            'transaction_sum': transaction_amount_in_crypto_wallet
        }

        balance_after_transaction =\
            "{:.2f}".format(float(crypto_wallet_balance_in_usd) - float(total_crypto_transaction_value_in_usd))
        form = SubmitWalletTransactionForm(initial=initial_data)

        if request.method == "POST" and request.user.is_authenticated:
            if float(crypto_wallet_balance_in_usd) >= float(total_crypto_transaction_value_in_usd):
                # wartość transakcji w walucie portfela (typ decimal)
                # transaction value in the wallet's currency (decimal type)
                decimal_value = "{:.2f}".format(Decimal(transaction_amount_in_crypto_wallet))
                wallet_instance.balance -= Decimal(decimal_value)
                wallet_instance.save()

                # tworzenie transakcji
                # creating the transaction
                new_transaction = Transaction(
                    user_id=request.user,
                    wallet=wallet_instance,
                    amount=amount,
                    transaction_type=Transaction.BUY,
                    purchased_currency=crypto,
                    status=Transaction.COMPLETED,
                    date=timezone.now(),
                    value_in_USD=total_crypto_transaction_value_in_usd,
                    balance_after_transaction=balance_after_transaction
                )

                new_transaction.save()
                messages.success(request, 'The transaction was successful')
                return HttpResponseRedirect(reverse('main:currency'))
            else:
                new_transaction = Transaction(
                    wallet=wallet_instance,
                    amount=amount,
                    transaction_type=Transaction.BUY,
                    purchased_currency=crypto,
                    status=Transaction.REJECTED,
                    date=timezone.now(),
                    value_in_USD=total_crypto_transaction_value_in_usd,
                    balance_after_transaction=crypto_wallet_balance_in_usd
                )
                new_transaction.save()
                messages.error(request, 'You do not have sufficient funds in your account')
    context = {
        'currency_rate': currency_rate,
        'crypto_rate': crypto_rate,
        'total_crypto_transaction_value': total_crypto_transaction_value_in_usd,
        'total_currency_transaction_value': total_currency_transaction_value_in_usd,
        'form': form

    }
    return render(request, 'wallet/transaction finalization.html', context)