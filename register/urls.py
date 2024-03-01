from django.urls import path
from main.views import currency_view
from .views import register, activate_account

app_name = 'register'

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate_account'),
    path('', currency_view, name='home')
]