from sellor.apps.products.models import Product


class Cart:
    def __init__(self, request) -> None:
        self.session = request.session
        cart = self.session.get('cart')
        if 'cart' not in request.session:
            cart = self.session['cart'] = []
        self.cart = cart

    def __iter__(self):
        products = Product.objects.filter(id__in=self.cart)
        for product in products:
            yield product

    def __len__(self):
        return len(self.cart)

    def add_item(self, product_id):
        if product_id not in self.cart:
            self.cart.append(product_id)
            self.save()
    
    def remove_item(self, product_id):
        self.cart.remove(product_id)
        self.save()

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True

    @property
    def items_qty(self):
        return len(self.cart)