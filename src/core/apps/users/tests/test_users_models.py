import pytest

from django.urls import reverse
from tests.models_setup import ModelsSetUp

from core.apps.users.models import ReportUser


def test_user_str_method(user_account):
    assert str(user_account) == 'user@gmail.com'


def test_user_get_absolute_url_method(user_account):
    assert user_account.get_absolute_url() == reverse('users:profile', args=[user_account.id])


def test_superuser_str_method(superuser_account):
    assert str(superuser_account) == 'admin@admin.com'


@pytest.mark.django_db
def test_user_create_no_email_given(user_account_factory):
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(email='')
    assert str(error.value) == 'Email is required' 


@pytest.mark.django_db
def test_user_create_short_password_given(user_account_factory):
    with pytest.raises(ValueError) as error:
        user_account = user_account_factory.create(password='12345')
    assert str(error.value) == 'Password must be at least 6 chars length.' 


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_superuser_str_method(user_account_factory):
    with pytest.raises(ValueError) as error:
        superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=False, is_superuser=True)
    assert str(error.value) == 'Superuser\'s "is_staff" must be set to True'

    with pytest.raises(ValueError) as error:
        superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=True, is_superuser=False)
    assert str(error.value) == 'Superuser\'s "is_superuser" must be set to True'


@pytest.mark.django_db
@pytest.mark.django_db
def test_superuser_create(user_account_factory):
    superuser_account = user_account_factory.create(email='admin@admin.com', is_staff=True, is_superuser=True)
    assert str(superuser_account) == 'admin@admin.com'


@pytest.mark.django_db
@pytest.mark.django_db
def test_user_fullname_method(user_account_factory):
    user = user_account_factory.create(first_name='John', last_name='Wick')
    assert user.fullname == 'John Wick'


class UserAccountTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.user.blacklist.blocked_users.add(self.user2)
        self.report = ReportUser.objects.create(
            report_author=self.user,
            user_reported=self.user2,
            reported_message=self.message
        )

    def test_user_chats_count_property(self):
        assert self.user.chats_count == '1'

    def test_user_sold_count_property(self):
        assert self.user.sold_count == 1
        assert self.user2.sold_count == 0
    
    def test_user_sold_total_property(self):
        assert self.user.sold_total == self.product2.current_price
        assert self.user2.sold_total == 0

    def test_user_purchased_count_property(self):
        assert self.user.purchased_count == 0
        assert self.user2.purchased_count == 1
    
    def test_user_purchased_total_property(self):
        assert self.user.purchased_total == 0
        assert self.user2.purchased_total == self.product2.current_price
    
    def test_user_is_blocked_by_method(self):        
        assert self.user2.is_blocked_by(self.user) == True
        assert self.user.is_blocked_by(self.user2) == False
    
    def test_user_has_blocked_method(self):
        assert self.user.has_blocked(self.user2) == True
        assert self.user2.has_blocked(self.user) == False

    def test_user_unseen_messages_count_property(self):
        assert self.user.unseen_messages_count == 4
    
    def test_user_blacklist_str_method(self):
        assert str(self.user.blacklist) == str(self.user)
    
    def test_user_report_user_str_method(self):
        assert str(self.report) == str(self.user2)

