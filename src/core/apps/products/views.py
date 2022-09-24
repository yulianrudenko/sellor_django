from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from core.utils import previous_url_or_other, available_products
from core.apps.users.models import Visitor
from .models import Product, Category, Tag
from .forms import ProductForm


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def category(request, category_name):
    category = get_object_or_404(Category, slug=category_name)
    products = available_products(request, Product.active_products.filter(category=category))
    product_paginator = Paginator(products, 10)
    products_page = product_paginator.get_page(request.GET.get('page'))
    context = {'category_name': category.name, 'page_obj': products_page}
    return render(request, 'products/category.html', context)


def product_all(request):
    ip_addr = get_client_ip(request)
    visitor, created = Visitor.objects.get_or_create(ip=ip_addr)
    products = available_products(request, Product.active_products).select_related('user')
    paginator = Paginator(products, 10)
    products_page = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': products_page}
    return render(request, 'products/home.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, purchased_by=None)
    if request.user.is_authenticated:
        if product.user in request.user.blacklist.blocked_users.all() or request.user in product.user.blacklist.blocked_users.all():
            messages.warning(request, _('This product is not available.'))
            return previous_url_or_other(request, reverse('products:home'))
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@login_required
def product_add(request):
    if request.method == 'POST':
        create_form = ProductForm(request.POST, request.FILES, user=request.user)
        if create_form.is_valid():
            new_product = create_form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            new_product.tags.add(*create_form.cleaned_data.get('tags'))
            messages.success(request, _('Product succesfully created.'))
            return redirect('products:detail', new_product.id)
    else:
        create_form = ProductForm()
    context = {'form': create_form}
    return render(request, 'products/product_create.html', context)


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, purchased_by=None)
    if product.user != request.user:
        return HttpResponseForbidden('You don\'t have permission to access this resource')
    if request.method == 'POST':
        edit_form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if edit_form.is_valid():
            product = edit_form.save()
            messages.success(request, _('Product succesfully updated. ') + f'<a href="{product.get_absolute_url()}" class="text-decoration-underline">' + _('See') + '</a>')
    else:
        edit_form = ProductForm(instance=product)
    context = {'form': edit_form, 'product': product}
    return render(request, 'products/product_edit.html', context)
    

@login_required
def remove_image(request, pk):
    product = get_object_or_404(Product, pk=pk, user=request.user.id, purchased_by=None)
    product.image = '../static/images/blank.jpg'
    product.save()
    messages.success(request, _('Image deleted.'))
    return redirect('products:edit', pk)


@login_required
def product_remove(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user != product.user:
        return HttpResponseForbidden('You don\'t have permission to access this resource')
    if request.method == 'POST':
        product.delete()
        messages.success(request, _('Product removed.'))
        return redirect('products:home')
    context = {'product': product}
    return render(request, 'products/product_remove_confirm.html', context)
