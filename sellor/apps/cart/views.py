from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .cart import Cart


def add_to_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'add_to_cart':
        product_id = request.POST['product_id']
        print(product_id)
        cart.add_item(product_id)
    response = {'qty': len(cart)}
    return JsonResponse(response)


def remove_from_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'remove_from_cart':
        product_id = request.POST['product_id']
        cart.remove_item(product_id)
    response = {'qty': len(cart), 'new_total_price': cart.get_total_price()}
    return JsonResponse(response)


def select_shipping(request):
    cart = Cart(request)
    response = {}
    if request.POST.get('action') == 'select_shipping':
        shipping_type_id = request.POST.get('shipping_id')
        if shipping_type_id != 0:
            cart.session['shipping_type_id'] = shipping_type_id
        else:
            del cart.session['shipping_type_id']
        cart.save()
    response = {'new_total_price': cart.get_total_price(), 'shipping_price': cart.get_shipping_price()}
    return JsonResponse(response)
    

def clear_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'clear_cart':
        cart.clear()
    response = {'qty': 0}
    return JsonResponse(response)


def remove_coupon_code(request):
    cart = Cart(request)
    print(cart.session['coupon_code'])
    del cart.session['coupon_code']
    cart.save()
    return redirect('users:cart')
