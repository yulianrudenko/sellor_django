from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


SHIPPING_CHOICES = [
    ('same day delivery', 'Same day delivery'),
    ('overnight delivery', 'Overnight delivery'),
    ('slow delivery', 'Slow delivery'),
]

class Shipping(models.Model):
    type = models.CharField(verbose_name=_('shipping type'), choices=SHIPPING_CHOICES, max_length=50, unique=True)
    description = models.CharField(verbose_name=_('shipping type description'), max_length=150)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.type}'


class Order(models.Model):
    user = models.ForeignKey('users.UserAccount', related_name='orders', on_delete=models.SET_NULL, null=True, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2) 
    shipping = models.ForeignKey(Shipping, related_name='orders', on_delete=models.SET_NULL, null=True)
    is_completed = models.BooleanField(default=False)  # whether user has payed for order or not

    def __str__(self) -> str:
        return f'{self.user.email} - {self.price}zl.'
