from django.urls import path
from .views import crypto_token, crypto_token_details, chosen_crypto_news

app_name = 'crypto'
urlpatterns = [
    path('', crypto_token, name='list'),
    path('<int:crypto_id>', crypto_token_details, name='details'),
    path('crypto-news', chosen_crypto_news, name='news')
]