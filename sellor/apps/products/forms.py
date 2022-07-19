from django import forms
from django.utils.translation import gettext_lazy as _


from .models import Product, Category, Tag, CATEGORY_CHOICES, TAG_CHOICES

class ProductForm(forms.ModelForm):
    title = forms.CharField(max_length=50)
    image = forms.FileField(label=_('Product picture'), widget=forms.FileInput(attrs={'onchange': 'readURL(this);'}), required=False)
    category = forms.ModelChoiceField(widget=forms.Select(), queryset=Category.objects.all(), required=True)
    description = forms.CharField(label=_('Description'), max_length=300, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}), required=False)
    tags = forms.ModelMultipleChoiceField(widget=forms.SelectMultiple(attrs={'class': 'form-control'}), queryset=Tag.objects.all(), required=False)

    def __init__(self, *args, **kwargs) -> None:
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['category'].widget.attrs['class'] = 'form-select'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['discount_price'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ['title', 'category', 'price', 'discount_price', 'description', 'tags', 'image']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if Product.objects.filter(user=self.user).exclude(id=self.instance.id).filter(title=title).exists():
            self.add_error('title', 'You already have product with given title, please rename product.')
        discount_p = cleaned_data.get('discount_price')
        if discount_p and discount_p >= cleaned_data.get('price'):
            self.add_error('discount_price', 'Discount price cannot be higher or same as regular.')
        return cleaned_data
