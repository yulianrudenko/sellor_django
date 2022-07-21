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
def product_add(request):
    if request.method == 'POST':
        create_form = ProductForm(request.POST, request.FILES, user=request.user)
        if create_form.is_valid():
            new_product = create_form.save(commit=False)
            new_product.user = request.user
            new_product.save()
            product_detail_url = reverse('products:detail', args=[new_product.id])
            messages.success(request, f'Product succesfully created. <a href={product_detail_url}>See</a>')
    else:
        create_form = ProductForm()
    context = {'form': create_form}
    return render(request, 'products/product_create.html', context)


@login_required
def product_edit(request, uid):
    product = get_object_or_404(Product, id=uid)
    if product.user != request.user:
        return redirect(reverse('products:detail', args=[uid]))
    if request.method == 'POST':
        edit_form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
        if edit_form.is_valid():
            product = edit_form.save()
            messages.success(request, f'Product succesfully updated. <a href="{product.get_absolute_url()}">See</a>')
    else:
        edit_form = ProductForm(instance=product)
    context = {'form': edit_form, 'product': product}
    return render(request, 'products/product_edit.html', context)
    


@login_required
def product_remove(request, uid):
    product = get_object_or_404(Product, id=uid)
    if request.user == product.user:
        if request.method == 'POST':
                product.delete()
                messages.success(request, 'Product removed.')
        else:
            context = {'product': product}
            return render(request, 'products/product_remove_confirm.html', context)
    return redirect('products:home')


def category(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    context = {'category': category, 'test': 'test'}
    return render(request, 'products/category.html', context)