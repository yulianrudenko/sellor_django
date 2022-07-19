from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from sellor.apps.products.models import (
    Product,
    Category,
    Tag,
    CouponCode
)
from sellor.apps.orders.models import Shipping, Order

User = get_user_model()
from django.db import connection


class ModelsSetUp(TestCase):
    def setUp(self) -> None:
        # dict for form tests
        self.credentials = {
            'email': 'user@gmail.com',
            'first_name': 'officer',
            'last_name': 'key',
            'password': '123456',
            'gender': 'M',
            'location': 'NY',
        }
        self.user = User.objects.create(**self.credentials)
        self.user.set_password(self.credentials['password'])
        self.user.save()
        
        self.user2 = User.objects.create(
            email='user2@gmail.com',
            first_name='lionel',
            last_name='messi',
            gender='M',
            location='Paris',
        )
        self.user2.set_password(self.credentials['password'])
        self.user2.save()

        # restarting the table sequence so category will have id=1 for each test   
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE products_category_id_seq RESTART WITH 1;")
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
        self.product.tags.add(self.tag)
        self.coupon = CouponCode.objects.create(
            code = 'test_coupon_code',
            reduce_amount = 5
        )
        self.shipping = Shipping.objects.create(
            type='same day delivery',
            description='test_description',
            price=100
        )
        self.order = Order.objects.create(
            user=self.user,
            price=100,
            shipping=self.shipping,
            is_completed=True
        )


class SimulateCart(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.get(reverse('products:home'))
        s = self.client.session
        s.update({'cart': [str(self.product.id)]})
        s.save()
