from django.test import TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from core.apps.products.models import Product, Category
from tests.models_setup import ModelsSetUp

User = get_user_model()

@override_settings(DEBUG=True)
class RegistrationTests(TestCase):
    def setUp(self) -> None:
        self.url = reverse('users:register')

    def test_registration_page(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'users/auth/register.html')
        assert response.status_code == 200

    def test_registration_post_success(self):
        response = self.client.post(self.url, data={
            'email': 'newuser@gmail.com',
            'first_name': 'officer',
            'last_name': 'key',
            'gender': 'M',
            'location': '1',
            'password1': '123456',
            'password2': '123456',
        })
        assert response.status_code == 200
        User = get_user_model()
        assert User.objects.first().fullname == 'Officer Key'
    
    def test_registration_error(self):
        response = self.client.post(self.url, data={
            'email': 'newuser@gmail.com',
            'first_name': 'officer',
            'last_name': 'key',
            'gender': 'M',
            'location': '1',
            'password1': '123456',
            'password2': 'incorrect_password2',
        })
        self.assertContains(response, 'Passwords do not match.')


class LoginLogoutTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('users:login')

    def test_login_page(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'users/auth/login.html')

    def test_login_post_success(self):
        response = self.client.post(self.url, {'email': self.credentials['email'], 'password': self.credentials['password']}, follow=True)
        assert response.status_code == 200
        assert response.context['user'].is_authenticated == True
        response_html = response.content.decode('utf-8')
        assert 'You have been logged in' in response_html
    
    def test_login_post_redirect_to_next_if_success(self):
        wishlist_url = reverse('users:wishlist')
        login_and_redirect_then_to_wishlist_url = f"{reverse('users:login')}?next={wishlist_url}"
        response = self.client.get(wishlist_url)
        assert response.status_code == 302 # should be redirected because unauthenticated trying to access wishlist 
        assert response.headers['location'] == login_and_redirect_then_to_wishlist_url  # url we should get in this case
        response = self.client.post(login_and_redirect_then_to_wishlist_url, {'email': 'user@gmail.com', 'password': '123456'}, follow=True)
        assert response.status_code == 200
        response_html = response.content.decode('utf-8')
        assert 'You have been logged in' in response_html
        assert response.request['PATH_INFO'] == wishlist_url

    def test_login_post_wrong_password(self):
        response = self.client.post(self.url, {'email': 'user@gmail.com', 'password': 'some_wrong_password'}, follow=True)
        assert response.status_code == 200
        assert response.context['user'].is_authenticated == False
        self.assertContains(response, 'Wrong password.')
    
    def test_login_post_account_is_not_activated(self):
        self.user.is_activated = False
        self.user.save()
        response = self.client.post(self.url, {'email': self.credentials['email'], 'password': self.credentials['password']}, follow=True)
        assert response.status_code == 200
        assert response.context['user'].is_authenticated == False
        response_html = response.content.decode('utf-8')
        assert 'You haven\'t activated your account.' in response_html

    def test_logout(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:logout'))
        assert response.status_code == 302
        assert response.headers['location'] == reverse('users:login')


class EditProfileTests(ModelsSetUp):
    def setUp(self) -> None:
        self.url = reverse('users:edit_profile')
        super().setUp()
        self.client.force_login(self.user)  # log user in to use in test

    def test_edit_profile_page(self):
        response = self.client.get(self.url)
        assert response.status_code == 200

    def test_edit_profile_post_success(self):
        first_name: str = 'john'
        response = self.client.post(self.url, {**self.credentials, 'first_name': first_name, 'location': self.city.id}, follow=True)
        assert response.status_code == 200
        self.user.refresh_from_db()
        assert self.user.first_name == first_name.capitalize()


class ChangePasswordTests(ModelsSetUp):
    def setUp(self) -> None:
        self.url = reverse('users:change_password')
        super().setUp()
        self.client.force_login(self.user)  # log user in to use in test
    
    def test_changepwd_page(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert str(response.context['user']) == self.credentials['email']
    
    def test_changepwd_post_success(self):
        current_password: str = '123456'
        new_password: str = 'new_password'
        assert self.user.check_password(current_password) == True
        password_form = {
            'current_password': current_password,
            'new_password': new_password,
            'verify_new_password': new_password
        }
        response = self.client.post(self.url, password_form, follow=True)
        assert response.status_code == 200
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == 'Please check your email (including "spam" section), we\'ve sent you message with confirmation link.'

class WishlistAddTests(ModelsSetUp):
    def setUp(self) -> None:
        # self.url = reverse('users:add_to_wishlist', args=)
        super().setUp()
        self.client.force_login(self.user2)  # log user in to use in test
        self.url = reverse('users:add_to_wishlist', args=[self.product.id])

    def test_add_to_wishlist_success_and_redirect_to_previous_page(self):
        product_url = reverse('products:detail', args=[self.product.id])
        self.client.get(product_url)
        response = self.client.get(self.url, {}, HTTP_REFERER=product_url)
        assert response.status_code == 302
        self.user.refresh_from_db()
        assert self.product in self.user2.wishlist.all()
        assert response.url == product_url  # because added prod to wishlist and want to stay there after that
        
    def test_add_to_wishlist_same_product_twice(self):
        response = self.client.get(self.url)
        assert response.status_code == 302
        response = self.client.get(self.url)
        assert response.status_code == 302
        messages = [str(message) for message in list(get_messages(response.wsgi_request))]
        assert 'Product already in wishlist.' in messages
    

class WishlistRemoveTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user2)  # log user in to use in test
        self.client.get(reverse('users:add_to_wishlist', args=[self.product.id]))  # add single product to wishlist 
        self.url = reverse('users:remove_from_wishlist', args=[self.product.id])

    def test_remove_from_wishlist_page(self):
        response = self.client.get(reverse('users:remove_from_wishlist', args=[self.product.id]))
        assert response.status_code == 302
        messages = [str(message) for message in list(get_messages(response.wsgi_request))]
        assert 'Removed product from your wishlist.' in messages
        self.user2.refresh_from_db()
        assert not self.user2.wishlist.all()


    def test_remove_from_wishlist_success_and_redirect_to_previous_page(self):
        product_url = reverse('products:detail', args=[self.product.id])
        self.client.get(product_url)
        response = self.client.get(self.url, {}, HTTP_REFERER=product_url)
        assert response.status_code == 302
        self.user2.refresh_from_db()
        assert not self.user2.wishlist.all()
        assert response.url == product_url  # because removed prod from wishlist and want to stay there after that


class UserProfileTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse('users:profile', args=[self.user2.id])
        self.client.force_login(self.user)

    def test_user_profile_page_success(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
    
    def test_user_profile_page_blacklist1(self):
        self.user.blacklist.blocked_users.add(self.user2)
        response = self.client.get(self.url)
        assert response.status_code == 302

    def test_user_profile_page_blacklist2(self):
        self.user2.blacklist.blocked_users.add(self.user)
        response = self.client.get(self.url)
        assert response.status_code == 302


class UserDashboardTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse('users:dashboard')

    def test_user_dashboard_page(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
        assert response.context['sold_products']
        assert not response.context['purchased_products']


class UserBlockTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)
        self.user.blacklist.blocked_users.add(self.user2)

    def test_blocked_users_page(self):
        response = self.client.get(reverse('users:blocked'))
        assert response.status_code == 200
        assert len(response.context['page_obj']) == 1

    def test_unblock_user(self):
        response = self.client.get(reverse('users:unblock', args=[self.user2.id]))
        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert 'Unblocked' in str(messages[0])


class ReportUsetTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_user_report_page(self):
        response = self.client.get(reverse('users:report', args=[self.user2.id]))
        assert response.status_code == 200

    def test_already_reported(self):
        self.user.blacklist.blocked_users.add(self.user2)
        response = self.client.get(reverse('users:report', args=[self.user2.id]))
        assert response.status_code == 302
        messages = list(get_messages(response.wsgi_request))
        assert f'You\'ve already blocked {self.user2.fullname}.' in str(messages[0])

    def test_user_report_by_message(self):
        response = self.client.get(reverse('users:report', args=[self.user2.id, self.message.id]))
        assert response.status_code == 200
        assert response.context['reported_message'] == self.message.text 
        # if user that is not member of chat tries to report a message
        self.client.force_login(self.user_extra)
        response = self.client.get(reverse('users:report', args=[self.user2.id, self.message.id]))
        assert response.status_code == 403

    def test_user_report_post(self):
        response = self.client.post(
            reverse('users:report', args=[self.user2.id]),
            data={
                'reported_message': self.message.id,
                'confirmation': 'YES'
            }
        )
        assert response.status_code == 302
        assert response.url == reverse('products:home') 