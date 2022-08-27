import pytest
from pytest_factoryboy import register
from tests.factories import (
    CityFactory,
    UserAccountFactory,
    ProductFactory,
    CategoryFactory,
)


register(CityFactory)
register(UserAccountFactory)
register(ProductFactory)
register(CategoryFactory)

@pytest.fixture
def city(db, city_factory):
    city = city_factory.create()
    return city

@pytest.fixture
def user_account(db, user_account_factory):
    user_account = user_account_factory.create()
    return user_account

@pytest.fixture
def superuser_account(db, user_account_factory):
    superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=True, is_superuser=True)
    return superuser_account


@pytest.fixture
def product(db, product_factory):
    product = product_factory.create()
    return product

@pytest.fixture
def category(db, category_factory):
    category = category_factory.create()
    return category
