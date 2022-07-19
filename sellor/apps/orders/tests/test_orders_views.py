from django.urls import reverse

from tests.models_setup import ModelsSetUp


class OrdersViewsTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_checkout_page(self):
        s = self.client.session
        s.update({
            'shipping_type_id': '1',
        })
        s.save()
        response = self.client.get(reverse('orders:checkout'), follow=True)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'orders/checkout.html')


    def test_checkout_redirect_cart_if_no_shipping_selected(self):
        response = self.client.get(reverse('orders:checkout'), follow=True)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'users/cart.html')

