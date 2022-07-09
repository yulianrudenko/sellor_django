from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from sellor.apps.products.models import (
    Product,
    Category,
    Tag,
    Review
)
from test_products_models import ModelsSetUp


User = get_user_model()

class ProductViewTest(ModelsSetUp):    
    def test_product_all_page(self):
        response = self.client.get(reverse('products:home'))
        assert response.status_code == 200
        assert str(response.context[0]['products'][0]) == str(self.product)
    
    def test_product_detail_page(self):
        response = self.client.get(reverse('products:detail', args=[self.product.id]))
        assert response.status_code == 200
        assert 'Test_product' in str(response.context[0]['product'])
    
    def test_product_remove_view_success(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('products:remove', args=[self.product.id]))
        assert response.status_code == 302
        assert not Product.objects.all()
    
    def test_product_remove_view_success_and_redirect_to_previous_page(self):
        self.client.force_login(self.user)
        previous_url = reverse('users:profile', args=[self.user.id])
        response = self.client.get(reverse('products:remove', args=[self.product.id]), {}, HTTP_REFERER=previous_url)
        assert response.status_code == 302
        assert response.url == previous_url


class CategoryViewTest(ModelsSetUp):    
    def test_category_page(self):
        response = self.client.get(reverse('products:category', args=[self.category.id]))
        assert response.status_code == 200
        assert 'test_category' in str(response.context[0]['category'])