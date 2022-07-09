import pytest

from django.urls import reverse


def test_user_str_method(user_account):
    assert str(user_account) == 'user@gmail.com'


def test_superuser_str_method(superuser_account):
    assert str(superuser_account) == 'admin@admin.com'

def test_user_create_no_email_given(user_account_factory):
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(email='')
    assert str(error.value) == 'Email is required' 

def test_user_create_short_password_given(user_account_factory):
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(password='12345')
    assert str(error.value) == 'Password must be at least 6 chars length.' 


def test_user_create_invalid_firstname_lastname(user_account_factory):
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(first_name=999)
    assert str(error.value) == 'Either first and last name must be valid.' 

    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(last_name=999)
    assert str(error.value) == 'Either first and last name must be valid.' 
    
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(first_name='1nval1d')
    assert str(error.value) == 'Either first and last name must be valid.' 

    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(last_name='1nval1d')
    assert str(error.value) == 'Either first and last name must be valid.' 


def test_superuser_str_method(user_account_factory):
    with pytest.raises(ValueError) as error:
        superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=False, is_superuser=True)
    assert str(error.value) == 'Superuser\'s "is_staff" must be set to True'

    with pytest.raises(ValueError) as error:
        superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=True, is_superuser=False)
    assert str(error.value) == 'Superuser\'s "is_superuser" must be set to True'

@pytest.mark.django_db
def test_superuser_create(user_account_factory):
    superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=True, is_superuser=True)
    assert str(superuser_account) == 'admin@admin.com'


@pytest.mark.django_db
def test_user_fullname_method(user_account_factory):
    user = user_account_factory.create(first_name='John', last_name='Wick')
    assert user.fullname == 'John Wick'


def test_user_get_absolute_url(client, user_account):
    url = user_account.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 200
