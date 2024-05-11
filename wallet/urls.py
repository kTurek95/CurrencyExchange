from django.urls import path
from .views import wallet, wallet_balance, wallet_selection, prepare_and_process_wallet_transaction, wallet_transaction
app_name = 'wallet'
urlpatterns = [
    path('', wallet, name='info'),
    path('balance/', wallet_balance, name='balance'),
    path('selection/', wallet_selection, name='transactions'),
    path('transacion/', prepare_and_process_wallet_transaction, name='transaction'),
    path('finalization/', wallet_transaction, name='wallet_transaction')
]