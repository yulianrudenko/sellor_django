from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

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


def clear_cart(request):
    cart = Cart(request)
    if request.POST.get('action') == 'clear_cart':
        cart.clear()
    response = {'qty': 0}
    return JsonResponse(response)
