from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.apps.products.models import (
    Product,
    Category,
    Tag,
)
from tests.models_setup import ModelsSetUp


User = get_user_model()


class ProductsViewsTest(ModelsSetUp):    
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_product_all_page(self):
        response = self.client.get(reverse('products:home'))
        assert response.status_code == 200
        assert str(response.context[0]['page_obj'][0]) == str(self.product)
    
    def test_product_detail_page(self):
        response = self.client.get(reverse('products:detail', args=[self.product.id]))
        assert response.status_code == 200
        assert 'Test_product' in str(response.context[0]['product'])
    
    def test_product_detail_page_blacklist1(self):
        self.client.force_login(self.user2)
        self.user2.blacklist.blocked_users.add(self.user)
        response = self.client.get(reverse('products:detail', args=[self.product.id]))
        assert response.status_code == 302
        assert response.url == reverse('products:home')

    def test_product_detail_page_blacklist2(self):
        self.client.force_login(self.user2)
        self.user.blacklist.blocked_users.add(self.user2)
        response = self.client.get(reverse('products:detail', args=[self.product.id]))
        assert response.status_code == 302
        assert response.url == reverse('products:home')

    def test_product_add_page(self):
        response = self.client.get(reverse('products:add'))
        assert response.status_code == 200

    def test_product_add_view_success(self):
        self.product.delete()
        response = self.client.post(reverse('products:add'), data={
            'title': 'test_product',
            'category': str(self.category.id),
            'price': '50',
            'discount_price': '40',
            'description': 'test_description',
        })
        assert response.status_code == 200
        response_html = response.content.decode('utf-8')
        assert 'Product succesfully created.' in response_html
    
    def test_product_edit_page(self):
        response = self.client.get(reverse('products:edit', args=[self.product.id]))
        assert response.status_code == 200
        response_html = response.content.decode('utf-8')
        assert f'<span class="h1 fw-bold mb-0">Edit product - {self.product.title.title()}</span>' in response_html

        self.client.logout()
        self.client.force_login(self.user2)
        response = self.client.get(reverse('products:edit', args=[self.product.id]), follow=True)
        assert response.status_code == 403
    
    def test_product_edit_post_success(self):
        response = self.client.post(reverse('products:edit', args=[self.product.id]), data={
            'title': 'test_product_edited',
            'category': str(self.category.id),
            'price': '1',
            'discount_price': '0',
            'description': 'test_description_edited',
        }, follow=True)
        assert response.status_code == 200
        assert Product.objects.get(id=self.product.id).title == 'Test_product_edited'
        response_html = response.content.decode('utf-8')
        assert 'Product succesfully updated.' in response_html

    def test_product_remove_page(self):
        response = self.client.get(reverse('products:remove', args=[self.product.id]))
        assert response.status_code == 200
        response_html = response.content.decode('utf-8')
        assert f'<span class="h1 fw-bold mb-0">Are You sure you want to delete <a href="{self.product.get_absolute_url()}"><i>{self.product.title}?</i></a></span>' in response_html
        self.assertTemplateUsed(response, 'products/product_remove_confirm.html')

    def test_product_remove_post_success(self):
        response = self.client.post(reverse('products:remove', args=[self.product.id]))
        assert response.status_code == 302
        assert Product.objects.count() == 1
        assert not Product.objects.filter(id=self.product.id)
    
    def test_product_remove_forbidden(self):
        self.client.force_login(self.user2)
        response = self.client.get(reverse('products:remove', args=[self.product.id]))
        assert response.status_code == 403


class CategoryViewTest(ModelsSetUp):    
    def test_category_page(self):
        response = self.client.get(reverse('products:category', args=[self.category.name]))
        assert response.status_code == 200
        assert 'test_category' == str(response.context[0]['category_name'])
    
    def test_category_page_blacklist1(self):
        self.client.force_login(self.user2)
        self.user2.blacklist.blocked_users.add(self.user)
        response = self.client.get(reverse('products:category', args=[self.category.name]))
        assert response.status_code == 200
        assert len(response.context[0]['page_obj']) == 0

    def test_category_page_blacklist2(self):
        self.client.force_login(self.user2)
        self.user.blacklist.blocked_users.add(self.user2)
        response = self.client.get(reverse('products:category', args=[self.category.name]))
        assert response.status_code == 200
        assert len(response.context[0]['page_obj']) == 0