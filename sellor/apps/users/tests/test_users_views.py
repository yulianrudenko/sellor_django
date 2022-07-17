from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

from sellor.apps.products.models import Product, Category
from tests.models_setup import ModelsSetUp, SimulateCart

User = get_user_model()

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
            'location': 'NY',
            'password1': '123456',
            'password2': '123456',
        })
        assert response.status_code == 302
        User = get_user_model()
        assert User.objects.first().fullname == 'Officer Key'
    
    def test_registration_error(self):
        response = self.client.post(self.url, data={
            'email': 'newuser@gmail.com',
            'first_name': 'officer',
            'last_name': 'key',
            'gender': 'M',
            'location': 'NY',
            'password1': '123456',
            'password2': 'incorrect_password2',
        })
        self.assertContains(response, 'Something want wrong. Please try again.')


# class RegisteredUserSetUp(TestCase):
#     '''
#     Help-class sets up registered user, with credentials ready to log in with, for feature tests
#     '''
#     def setUp(self) -> None:
#         User = get_user_model()
#         self.credentials = {
#             'email': 'user@gmail.com',
#             'first_name': 'officer',
#             'last_name': 'key',
#             'password': '123456',
#             'gender': 'M',
#             'location': 'NY',
#         }
#         self.user = User.objects.create(**self.credentials)
#         self.user.set_password(self.credentials['password'])
#         self.user.save()


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
        User = get_user_model()
        response = self.client.post(self.url, {'email': 'user@gmail.com', 'password': 'some_wrong_password'}, follow=True)
        assert response.status_code == 200
        assert response.context['user'].is_authenticated == False
        self.assertContains(response, 'Wrong password.')

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
        response = self.client.post(self.url, {**self.credentials, 'first_name': first_name}, follow=True)
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
        self.user.refresh_from_db()
        assert self.user.check_password(new_password) == True


class WishlistAddTests(ModelsSetUp):
    def setUp(self) -> None:
        # self.url = reverse('users:add_to_wishlist', args=)
        super().setUp()
        self.client.force_login(self.user)  # log user in to use in test
        self.url = reverse('users:add_to_wishlist', args=[self.product.id])

    def test_add_to_wishlist_success_and_redirect_to_previous_page(self):
        product_url = reverse('products:detail', args=[self.product.id])
        self.client.get(product_url)
        response = self.client.get(self.url, {}, HTTP_REFERER=product_url)
        assert response.status_code == 302
        self.user.refresh_from_db()
        assert self.product in self.user.wishlist.all()
        assert response.url == product_url  # because added prod to wishlist and want to stay there after that
        
    def test_add_to_wishlist_same_product_twice(self):
        response = self.client.get(self.url)
        assert response.status_code == 302
        response = self.client.get(self.url)
        assert response.status_code == 302
        messages = [str(message) for message in list(get_messages(response.wsgi_request))]
        assert 'Product already in wishlist' in messages
    

class WishlistRemoveTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)  # log user in to use in test
        self.client.get(reverse('users:add_to_wishlist', args=[self.product.id]))  # add single product to wishlist 
        self.url = reverse('users:remove_from_wishlist', args=[self.product.id])

    def test_remove_from_wishlist_page(self):
        response = self.client.get(reverse('users:remove_from_wishlist', args=[self.product.id]))
        assert response.status_code == 302
        messages = [str(message) for message in list(get_messages(response.wsgi_request))]
        assert 'Removed product from your wishlist' in messages
        self.user.refresh_from_db()
        assert not self.user.wishlist.all()


    def test_remove_from_wishlist_success_and_redirect_to_previous_page(self):
        product_url = reverse('products:detail', args=[self.product.id])
        self.client.get(product_url)
        response = self.client.get(self.url, {}, HTTP_REFERER=product_url)
        assert response.status_code == 302
        self.user.refresh_from_db()
        assert not self.user.wishlist.all()
        assert response.url == product_url  # because removed prod from wishlist and want to stay there after that


class CartTests(SimulateCart):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)
        self.url = reverse('users:cart')

    def test_cart_page_success(self):
        response = self.client.get(self.url)
        assert response.status_code == 200
    
    def test_cart_coupon_post_success(self):
        coupon_code: str = 'john'
        response = self.client.post(self.url, {'coupon_code': self.coupon.code}, follow=True)
        assert response.status_code == 200
        assert self.client.session.get('coupon_code') == 'test_coupon_code'

    def test_cart_coupon_post_doesnt_exist_error(self):
        self.coupon.delete()
        response = self.client.post(self.url, {'coupon_code': self.coupon.code}, follow=True)
        assert response.status_code == 200
        assert self.client.session.get('coupon_code') == None
        response_html = response.content.decode('utf-8')
        assert 'This code doesn\'t exist.' in response_html


    def test_cart_coupon_post_used_coupon_error(self):
        self.user.used_coupones.add(self.coupon)
        response = self.client.post(self.url, {'coupon_code': self.coupon.code}, follow=True)
        assert response.status_code == 200
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You have already used this coupone')

    def test_cart_shipping_form_filled_if_shipping_set(self):
        s = self.client.session
        s.update({'shipping_type_id': self.shipping.id})
        s.save()
        response = self.client.get(self.url)
        response_html: str = response.content.decode('utf-8')
        assert f' selected>{self.shipping.type}</option>' in response_html
