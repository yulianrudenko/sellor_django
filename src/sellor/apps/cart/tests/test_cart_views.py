from django.urls import reverse

from tests.models_setup import ModelsSetUp


class CartViewsTests(ModelsSetUp):
    def add_product_to_cart(self):
        response = self.client.post(reverse('cart:add'), data={
            'product_id': self.product.id,
            'action': 'add_to_cart'
        })
        return response
    
    def select_shipping_type(self):
        response = self.client.post(reverse('cart:select_shipping'), data={
            'shipping_id': self.shipping.id,
            'action': 'select_shipping'
        })
        return response

    def test_add_to_cart(self):
        response = self.add_product_to_cart()
        assert response.json().get('qty') == 1
    
    def test_remove_from_cart(self):
        self.add_product_to_cart()
        response = self.client.post(reverse('cart:remove'), data={
            'product_id': self.product.id,
            'action': 'remove_from_cart'
        })
        assert response.json().get('qty') == 0

    def test_select_shipping_success(self):
        self.add_product_to_cart()
        response = self.select_shipping_type()
        assert float(response.json().get('shipping_price')) == self.shipping.price

    def test_select_shipping_not_selected(self):
        self.add_product_to_cart()
        self.select_shipping_type()
        response = self.client.post(reverse('cart:select_shipping'), data={
            'shipping_id': 0,
            'action': 'select_shipping'
        })
        assert float(response.json().get('shipping_price')) == 0
    
    def test_clear_cart_success(self):
        self.add_product_to_cart()
        response = self.client.post(reverse('cart:clear'), data={
            'action': 'clear_cart'
        })
        assert response.json().get('qty') == 0
    
    def test_remove_coupon_code(self):
        # first need to add coupon
        self.client.force_login(self.user)
        response = self.client.post(reverse('users:cart'), data={'coupon_code': self.coupon.code})
        assert self.client.session.get('coupon_code') == self.coupon.code
        # now remove it
        response = self.client.get(reverse('cart:remove_coupon_code'))
        assert self.client.session.get('coupon_code') == None