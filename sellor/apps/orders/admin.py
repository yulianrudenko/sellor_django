from django.contrib import admin

from .models import Order, Shipping


admin.site.register(Order)
admin.site.register(Shipping)
