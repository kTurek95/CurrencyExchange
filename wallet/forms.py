from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Wallet, AvailableCurrency, CryptoTokenCurrency


class WalletTransactionForm(forms.ModelForm):
    currency = forms.ModelChoiceField(queryset=AvailableCurrency.objects.none(), required=False, label='Currency')
    crypto_currency = forms.ModelChoiceField(queryset=CryptoTokenCurrency.objects.all(), required=False,
                                             label='Crypto Currency')
    amount = forms.DecimalField()

    class Meta:
        model = Wallet
        fields = ['currency', 'crypto_currency', 'amount']

    def __init__(self, *args, **kwargs):
        currency_choices = kwargs.pop('currency_choices', None)
        super(WalletTransactionForm, self).__init__(*args, **kwargs)
        if currency_choices is not None:
            # Setting choices for the 'currency' field
            self.fields['currency'].queryset = currency_choices
            # Removing the 'crypto_currency' field, as we are dealing with regular currency
            del self.fields['crypto_currency']
        elif currency_choices is None:
            # If 'currency_choices' is None, we assume it's cryptocurrency
            # Removing the 'currency' field
            del self.fields['currency']
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.form_action = 'wallet_transaction'
        self.helper.add_input(Submit('submit', 'Submit'))


class SubmitWalletTransactionForm(forms.Form):
    wallet_balance = forms.DecimalField(disabled=True, required=False)
    wallet_balance_in_usd = forms.DecimalField(disabled=True, label='Balance in USD', required=False)
    selected_currency = forms.CharField(disabled=True, required=False)
    currency_amount = forms.DecimalField(disabled=True, required=False)
    currency_rate = forms.DecimalField(disabled=True, required=False)
    transaction_sum_in_usd = forms.DecimalField(disabled=True, required=False, label='Transaction sum in USD')
    transaction_sum = forms.DecimalField(disabled=True, required=False)

    class Meta:
        model = Wallet
        fields = [
            'wallet_balance_in_usd',
            'selected_currency',
            'currency_amount',
            'currency_rate',
            'transaction_sum',
            'submit_transaction'
        ]

    def __init__(self, *args, **kwargs):
        super(SubmitWalletTransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))


