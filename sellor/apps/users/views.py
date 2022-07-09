from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from sellor.apps.products.models import Product
from .models import UserAccount
from .forms import RegistrationForm, LoginForm, UserEditForm, UserChangePasswordForm
from .utils import redirect_home_if_authenticated, previous_url_or_other


@redirect_home_if_authenticated
def register(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password2'])
            new_user.save()
            new_user = authenticate(
                username=registration_form.cleaned_data['email'],
                password=registration_form.cleaned_data['password2'],
            )
            if new_user is not None:
                login(request, new_user)
                messages.info(request, "Thanks for registering &hearts; You are now logged in.")
                return redirect('home')
        messages.warning(request, 'Something want wrong. Please try again.')
    else:
        registration_form = RegistrationForm() 
    context = {'form': registration_form}
    return render(request, 'users/auth/register.html', context)


@redirect_home_if_authenticated
def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                username=login_form.cleaned_data['email'],
                password=login_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'Hello {user.first_name}! You have been logged in')
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('/')
            login_form.add_error('password', 'Wrong password.')
    else:
        login_form = LoginForm()
    return render(request, 'users/auth/login.html', context={'form': login_form})


def logout_user(request):
    logout(request)
    return redirect('users:login')


def user_profile(request, id: int):
    user = get_object_or_404(UserAccount, id=id)
    context = {'user': user}
    return render(request, 'users/user_profile.html', context)


@login_required
def edit_profile(request):
    user = get_object_or_404(UserAccount, id=request.user.id)
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            user = edit_form.save()
            edit_form = UserEditForm(instance=user)
    else:
        edit_form = UserEditForm(instance=user)
    context = {'user': user, 'form': edit_form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    user = get_object_or_404(UserAccount, id=request.user.id)
    if request.method == 'POST':
        # append POST data with user instance that wants to change password to validate compare input and real password
        data = request.POST.dict()
        data.update({'user': request.user})
        change_password_form = UserChangePasswordForm(data=data)
        if change_password_form.is_valid():
            user.set_password(change_password_form.cleaned_data['verify_new_password'])
            user.save()
            messages.success(request, 'Password changed. Please log in with new password.')
            return redirect('users:login')
    else:
        change_password_form = UserChangePasswordForm()
    context = {'user': user, 'form': change_password_form}
    return render(request, 'users/auth/change_password.html', context)


@login_required
def wishlist(request):
    user = request.user
    wishlist = user.wishlist.all()
    context = {
        'user': user,
        'wishlist': wishlist
    }
    return render(request, 'users/wishlist.html', context)


def cart(request):
    context = {}
    return render(request, 'users/cart.html', context)


@login_required
def add_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    if product in wishlist.all():
        messages.warning(request, 'Product already in wishlist')
    else:
        wishlist.add(product)
        messages.success(request, 'Added product to your wishlist')
    return previous_url_or_other(request, reverse('users:wishlist'))


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    if product in wishlist.all():
        wishlist.remove(product)
        messages.success(request, 'Removed product from your wishlist')
    return previous_url_or_other(request, reverse('products:detail', args=[product_id]))
