from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.apps.products.models import (
    Product,
    Category,
    Tag
)
from tests.models_setup import ModelsSetUp

User = get_user_model()


class ProductTests(ModelsSetUp):
    def test_product_str_method(self):
        assert str(self.product) == 'Test_product'
    
    def test_product_discount_percentage_property(self):
        discount_percentage = float(100 - ((100 * self.product.discount_price) / self.product.price))
        assert float(self.product.discount_percentage) == discount_percentage
    
    def test_product_get_absolute_url_method(self):
        assert self.product.get_absolute_url() == reverse('products:detail', args=[self.product.id])
    
    def test_product_discount_price_higher_than_regular(self):
        try:
            self.product.discount_price = 51
            self.product.save()
        except ValueError as err:
            assert str(err) == 'Discount price cannot be higher than regular.'
    
    def test_product_current_price(self):
        assert self.product.current_price == 40
        self.product.discount_price = None  # set disc.price to NULL
        assert self.product.current_price == 50
    
    def test_product_active_products_manager(self):
        assert Product.active_products.first() == self.product

    def test_product_is_active_property(self):
        self.product.save()
        assert self.product.is_active == True
        assert self.product2.is_active == False


class CategoryTests(ModelsSetUp):
    def test_category_str_method(self):
        assert str(self.category) == 'test_category'
    
    def test_category_get_absolute_url_method(self):
        assert self.category.get_absolute_url() == reverse('products:category', args=[self.category.name])

    def test_category_run_signals(self):
        assert self.category.save() == None
        assert self.category.delete()

class TagTests(ModelsSetUp):
    def test_tag_str_method(self):
        assert str(self.tag) == 'test_tag'
    
    def test_tag_run_signals(self):
        assert self.tag.save() == None
        assert self.tag.delete()
