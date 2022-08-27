import factory
from faker import Faker

from core.apps.users.models import UserAccount, City
from core.apps.products.models import (
    Product,
    Category,
    Tag
)
from core.apps.chats.models import Chat

fake = Faker()

class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
        django_get_or_create = ('name', )
    
    name = 'test_city'

class UserAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAccount
        django_get_or_create = ('email', )
    
    email = 'user@gmail.com'
    first_name = fake.first_name()
    last_name = fake.last_name()
    password = '123456'
    location = factory.SubFactory(CityFactory)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class=model_class)
        if 'is_superuser' in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name', )
    
    name = 'test_category'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('title',)
    
    user = factory.SubFactory(UserAccountFactory)
    category = factory.SubFactory(CategoryFactory)
    title = 'test_product'
    price = 50
    discount_price = 40
    description = 'description for test_product'

