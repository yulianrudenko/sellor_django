from sellor.apps.products.models import Product, CouponCode
from sellor.apps.orders.models import Shipping


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
    
    def get_shipping_price(self):
        shipping_type_id = self.session.get('shipping_type_id', '0')
        if shipping_type_id != '0':
            shipping_price = Shipping.objects.get(id=shipping_type_id).price
            return shipping_price
        return 0
    
    def get_shipping_type(self):
        shipping_type_id = self.session.get('shipping_type_id', '0')
        if shipping_type_id != '0':
            shipping_type = Shipping.objects.get(id=shipping_type_id).type
            return shipping_type
        return Shipping.objects.none()

    def get_total_price(self):
        total = 0
        for product_id in self.cart:
            total += Product.objects.get(id=product_id).current_price
        shipping_type_id = self.session.get('shipping_type_id', '0')
        if shipping_type_id != '0':
            shipping_price = Shipping.objects.get(id=shipping_type_id).price
            total += shipping_price
        if self.session.get('coupon_code'):
            total -= self.coupon_code.reduce_amount
        return total

    def get_subtotal_price(self):
        total = 0
        for product_id in self.cart:
            total += Product.objects.get(id=product_id).current_price
        return total
    
    @property
    def coupon_code(self):
        return CouponCode.objects.get(code=self.session.get('coupon_code')) 
    
    def code_is_activated(self):
        if self.session.get('coupon_code'):
            return True
        return False

    def clear(self):
        del self.session['cart']
        self.save()

    def save(self):
        self.session.modified = True

    @property
    def items_qty(self):
        return len(self.cart)