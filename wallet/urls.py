from django.urls import path
from .views import wallet, wallet_balance, wallet_selection, wallet_transaction
app_name = 'wallet'
urlpatterns = [
    path('', wallet, name='info'),
    path('balance/', wallet_balance, name='balance'),
    path('selection/', wallet_selection, name='transactions'),
    path('transacion/', wallet_transaction, name='transaction')
]