from tests.models_setup import ModelsSetUp
from core.apps.products.forms import ProductForm


class ProductFormTests(ModelsSetUp):
    def test_product_form_clean(self):
        form = ProductForm(data={
            'title': self.product.title,
            'category': self.product.category,
            'price': 2,
            'discount_price': 3
        }, user=self.user)
        assert 'You already have product with given title, please rename product.' and \
            'Discount price cannot be higher or same as regular.' in str(form.errors)
