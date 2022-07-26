from django import forms


class PaymentDataRequestForm(forms.Form):
    bankcard_number = forms.IntegerField(label='Bankcard number', min_value=1000_0000, max_value=9999_9999)
