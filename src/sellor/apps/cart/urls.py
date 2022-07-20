from django.urls import path

from . import views


app_name = 'cart'

urlpatterns = [
    path('add-to-cart', views.add_to_cart, name='add'),
    path('remove-from-cart', views.remove_from_cart, name='remove'),
    path('select-shipping', views.select_shipping, name='select_shipping'),
    path('clear-cart', views.clear_cart, name='clear'),
    path('remove-coupon-code', views.remove_coupon_code, name='remove_coupon_code'),
]
