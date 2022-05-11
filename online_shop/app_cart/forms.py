from django import forms
from django.core.exceptions import ValidationError

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddGoodForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput)
    max_quantity = forms.IntegerField()     #todo  widget=forms.HiddenInput скрыть поле

    def clean(self):
        super().clean()
        errors = {}
        if self.cleaned_data['quantity'] > self.cleaned_data['max_quantity']:
            errors['quantity'] = ValidationError('Quantity of goods is more than in storage')

        if errors:
            raise ValidationError(errors)
