from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from sellor.apps.orders.models import Shipping, Order
from tests.models_setup import ModelsSetUp

User = get_user_model()


class ShippingTests(ModelsSetUp):
    def test_shipping_str_method(self):
        assert str(self.shipping) == 'same day delivery'


class OrderTests(ModelsSetUp):
    def test_shipping_str_method(self):
        assert str(self.order) == 'user@gmail.com - 100zl.'
