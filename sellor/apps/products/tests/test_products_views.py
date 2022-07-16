from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from sellor.apps.products.models import (
    Product,
    Category,
    Tag,
)
from tests.models_setup import ModelsSetUp


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
        response = self.client.post(reverse('products:remove', args=[self.product.id]))
        assert response.status_code == 302
        assert not Product.objects.all()


class CategoryViewTest(ModelsSetUp):    
    def test_category_page(self):
        response = self.client.get(reverse('products:category', args=[self.category.id]))
        assert response.status_code == 200
        assert 'test_category' in str(response.context[0]['category'])