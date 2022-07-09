from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages

from sellor.apps.users.utils import previous_url_or_other
from .models import Product, Category, Tag
from .forms import ProductForm


def product_all(request):
    products = Product.objects.all().select_related('user')
    context = {'products': products}
    return render(request, 'products/home.html', context)


def product_detail(request, uid):
    product = Product.objects.select_related('user').get(id=uid)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@login_required
def product_edit(request, uid):
    product = get_object_or_404(Product, id=uid)
    if product.user == request.user:
        if request.method == 'POST':
            edit_form = ProductForm(request.POST, request.FILES, instance=product)
            if edit_form.is_valid():
                product = edit_form.save()
                messages.success(request, 'Product succesfully updated.')
        else:
            edit_form = ProductForm(instance=product)
        context = {'form': edit_form, 'product': product}
        return render(request, 'products/product_edit.html', context)
    return reverse('products:detail', args=[uid])


@login_required
def product_remove(request, uid):
    product = get_object_or_404(Product, id=uid)
    previous_url = request.META.get('HTTP_REFERER')
    if product.user == request.user:
        product.delete()
        if previous_url:
            if reverse('products:detail', args=[uid]) not in previous_url:
                return previous_url_or_other(request, reverse('products:home'))
        return redirect('products:home')
    return previous_url_or_other(request, reverse('products:detail', args=[uid]))


def category(request, id):
    category = get_object_or_404(Category, id=id)
    context = {'category': category, 'test': 'test'}
    return render(request, 'products/category.html', context)