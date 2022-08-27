from django import forms

from core.apps.products.models import Category, Tag
from core.apps.users.models import City


class ProductSearchForm(forms.Form):
    title = forms.CharField(max_length=40, required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)
    location = forms.ModelMultipleChoiceField(queryset=City.objects.all(), required=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['title'].widget.attrs['style'] = 'text-align: center; width: 75%'
        self.fields['category'].widget.attrs['class'] ='selectpicker'
        self.fields['tags'].widget.attrs['class'] = 'selectpicker'
        self.fields['tags'].widget.attrs['data-live-search'] = 'true'
        self.fields['location'].widget.attrs['class'] = 'selectpicker'
        self.fields['location'].widget.attrs['data-live-search'] = 'true'
