from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from sellor.apps.products.models import (
    Product,
    Category,
    Tag,
    Review
)


User = get_user_model()

class ModelsSetUp(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email = 'user@gmail.com',
            first_name = 'officer',
            last_name = 'key',
            gender='M',
            location='NY',
            password='123456',
        )
        self.category = Category.objects.create(
            name='test_category'
        )
        self.product = Product.objects.create(
            user=self.user,
            category=self.category,
            title='test_product',
            price=50,
            discount_price=40,
            description='description for test_product'
        )
        self.tag = Tag.objects.create(
            name='test_tag'
        )
        self.review = Review.objects.create(
            author=self.user,
            product=self.product,
            text='test_review',
            rating=5
        )


class ProductTests(ModelsSetUp):
    def test_product_str_method(self):
        assert str(self.product) == 'Test_product'
    
    def test_product_rating_property(self):
        assert self.product.rating == 5
        self.product.reviews.all().delete()
        assert self.product.rating == 0
    
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




class CategoryTests(ModelsSetUp):
    def test_category_str_method(self):
        assert str(self.category) == 'test_category'
    
    def test_category_get_absolute_url_method(self):
        assert self.category.get_absolute_url() == reverse('products:category', args=[self.category.id])


class TagTests(ModelsSetUp):
    def test_tag_str_method(self):
        assert str(self.tag) == 'test_tag'


class ReviewTests(ModelsSetUp):
    def test_review_str_method(self):
        assert str(self.review) == f'user@gmail.com for Test_product'
    