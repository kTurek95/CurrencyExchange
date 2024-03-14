"""
This module contains the views related to the CryptoTokenCurrency model in the Django application.

The views in this module are responsible for
handling the presentation layer of the crypto token currencies.
It includes views for listing all the available crypto tokens
and for displaying the details of a specific crypto token.
These views interact with the CryptoTokenCurrency model to retrieve data from the database,
and they render the appropriate templates with context data.

Functions:
    crypto_token(request): Renders a list of all crypto tokens with pagination.
    crypto_token_details(request, crypto_id): Renders the details of a specific crypto token.
"""


from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import CryptoTokenCurrency


def crypto_token(request):
    """
    View for listing all available crypto tokens.

    This view retrieves all crypto tokens from the database, orders them by their code,
    and paginates them with a fixed number of tokens per page
    (300 tokens per page).
    The view also handles the request to get a specific page of tokens.
    It then passes the paginated tokens and menu context
    to the crypto-token-list.html template for rendering.

    Args:
    request : HttpRequest
        The incoming request object from the user.

    Returns:
    HttpResponse
        Rendered web page with the list of crypto tokens and pagination controls.
    """
    crypto = CryptoTokenCurrency.objects.all().order_by('code')
    paginator = Paginator(crypto, 300)
    page_number = request.GET.get('page')
    crypto_tokens = paginator.get_page(page_number)
    context = {
        'crypto_token': crypto_tokens,
        'active_menu': 'Available Crypto/Tokens'}
    return render(request, 'CryptoCurrencies/crypto-token-list.html', context)


@ login_required
def crypto_token_details(request, crypto_id: int):
    """
    View for displaying the details of a specific crypto token.

    This view fetches the details of a specific crypto token identified by the `crypto_id`.
    It ensures that the user is logged in before accessing this view. If the token
    exists, its details along with the menu context are passed to the
    crypto-token-details.html template for rendering.

    Args:
    request : HttpRequest
        The incoming request object from the user.
    crypto_id : int
        The unique identifier of the crypto token whose details are to be retrieved.

    Returns:
    HttpResponse
        Rendered web page with the details of the specified crypto token.
    """
    crypto_details = CryptoTokenCurrency.objects.get(pk=crypto_id)
    context = {
        'crypto_token_details': crypto_details,
        'active_menu': 'Available Crypto/Tokens'}

    return render(request, 'CryptoCurrencies/crypto-token-details.html', context)
