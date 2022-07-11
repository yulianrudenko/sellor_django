from django import forms

from .models import Shipping


class ShippingForm(forms.Form):
    shipping_type = forms.ModelChoiceField(widget=forms.Select(), queryset=Shipping.objects.all(), required=True)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['shipping_type'].widget.attrs['class'] = 'select form-select'
        self.fields['shipping_type'].widget.attrs['id'] = 'shipping-type'