from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UsersUtilsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user('test@gmail.com', '123456', 'Joe', 'Sins')

    def test_redirect_home_if_authenticated_redirect(self):
        User = get_user_model()
        self.client.login(email='test@gmail.com', password='123456')
        response = self.client.get(reverse('users:register'))
        assert response.status_code == 302
    
    def test_redirect_home_if_authenticated_no_redirect(self):
        response = self.client.get(reverse('users:register'))
        assert response.status_code == 200