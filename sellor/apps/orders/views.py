from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def checkout(request):
    if not request.session.get('shipping_type_id') or request.session.get('shipping_type_id') == 0:
        messages.warning(request, 'Please select shipping type first.')
        return redirect('users:cart')
    return render(request, 'orders/checkout.html')