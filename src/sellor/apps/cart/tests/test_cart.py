from sellor.apps.cart.cart import Cart
from sellor.apps.products.models import Product, CouponCode
from sellor.apps.orders.models import Shipping

from tests.models_setup import ModelsSetUp
from django.contrib.sessions.backends.db import SessionStore


class SimulateRequest():
    def __init__(self) -> None:
        self.session = SessionStore()

request = SimulateRequest()


class CartTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.test_request = Cart(request)
    
    def add_item_to_cart(self):
        self.test_request.add_item(self.product.id)

    def test_add_remove_item(self):
        self.add_item_to_cart()
        assert self.test_request.cart[0] == self.product.id
        self.test_request.remove_item(self.product.id)
        assert self.test_request.cart == []
    
    def test_get_shipping_type(self):
        assert str(self.test_request.get_shipping_type()) == str(Shipping.objects.none())
        self.test_request.session['shipping_type_id'] = str(self.shipping.id)
        assert str(self.test_request.get_shipping_type()) == self.shipping.type
    
    def test_cart_clear(self):
        self.add_item_to_cart()
        self.test_request.clear()
        assert 'cart' not in self.test_request.session

    def test_get_subtotal_price(self):
        self.add_item_to_cart()
        assert self.test_request.get_subtotal_price() == self.product.current_price
