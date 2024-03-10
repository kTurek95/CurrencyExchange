from django.urls import path
# from .views import wallet, wallet_balance, wallet_selection, wallet_transaction
from .views import UserWallet as Uw

app_name = 'wallet'
urlpatterns = [
    path('', Uw.create_wallet, name='info'),
    path('balance/', Uw.wallet_balance, name='balance'),
    path('selection/', Uw.wallet_selection, name='transactions'),
    path('transacion/', Uw.wallet_transaction, name='transaction')
]