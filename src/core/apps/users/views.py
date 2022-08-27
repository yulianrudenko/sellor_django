from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import HttpResponseForbidden, JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.safestring import mark_safe

from core.apps.products.models import Product
from core.apps.chats.models import Chat, Message
from core.utils import redirect_home_if_authenticated, previous_url_or_other, available_products

from .models import UserAccount, ReportUser, Blacklist, Feedback
from .forms import RegistrationForm, LoginForm, UserEditForm, UserChangePasswordForm, ReportForm
from .token import activation_token 


def about_page(request):
    return render(request, 'about.html')


def feedback(request):
    user = request.user
    if request.method == 'POST':
        if user.is_authenticated:
            if user.feedbacks.all().count() >= 3:
                messages.warning(request, 'You can\'t post more than 3 feedbacks, please delete a few to post new one.')
            else:
                text = request.POST.get('feedback')
                if len(text) < 6 or len(text) > 250:
                    messages.warning(request, 'Please provide text between 6 and 250 characters.')
                else:
                    Feedback.objects.create(user=user, text=text)

    if user.is_authenticated:
        from django.db.models import Value, BooleanField, Case, When
        feedbacks = Feedback.objects.annotate(
            is_users=Case(
                When(user=request.user,
                    then=Value(True)),
                default=Value(False),
                output_field=BooleanField())
        ).order_by('-is_users', '-date_created')
    else:
        feedbacks = Feedback.objects.all().order_by('-date_created')
    context = {'posts': feedbacks}
    return render(request, 'feedback.html', context)


def upvote_feedback(request):
    if request.method == 'POST' and request.POST.get('userId') and request.POST.get('postId'):
        user_id = int(request.POST['userId'])
        feedback_id = int(request.POST['postId'])
        if UserAccount.objects.filter(id=user_id).exists():
            user = UserAccount.objects.filter(id=user_id)[0]
            if Feedback.objects.filter(id=feedback_id).exists():
                fdbck = Feedback.objects.filter(id=feedback_id)[0]
                if user != fdbck.user:
                    if  user not in fdbck.upvoted_by.all():
                        fdbck.upvoted_by.add(user)
                        return JsonResponse({'added': True, 'qty': fdbck.upvoted_by.count()})
                    else:
                        fdbck.upvoted_by.remove(user)
                        return JsonResponse({'deleted': True, 'qty': fdbck.upvoted_by.count()})
    return JsonResponse({'error': '0'})


def delete_feedback(request):
    if request.method == 'POST' and request.POST.get('userId') and request.POST.get('postId'):
        user_id = int(request.POST['userId'])
        feedback_id = int(request.POST['postId'])
        if UserAccount.objects.filter(id=user_id).exists():
            user = UserAccount.objects.filter(id=user_id)[0]
            if Feedback.objects.filter(id=feedback_id).exists():
                fdbck = Feedback.objects.filter(id=feedback_id)[0]
                if user == fdbck.user:
                    fdbck.delete()
                    return JsonResponse({'deleted': True})
    return JsonResponse({'error': '0'})


def send_activation_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('users/auth/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': activation_token.make_token(user)
    })
    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


def activate_user(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(UserAccount, pk=uid)
    if activation_token.check_token(user, token):
        user.is_activated = True
        user.save()
        messages.success(request, 'Email verified, You can now log in!')
        return redirect('users:login')
    messages.error(request, f'{user.first_name}, something went wrong with your email verification.')
    return redirect('users:register')


@redirect_home_if_authenticated
def register(request):
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST, request.FILES)
        if registration_form.is_valid():
            new_user = registration_form.save(commit=False)
            new_user.set_password(registration_form.cleaned_data['password2'])
            new_user.save()
            send_activation_email(request, new_user)
            messages.success(request, 'Please check your email (including "spam" section), we\'ve sent you message with an activation link.')
    else:
        registration_form = RegistrationForm() 
    context = {'form': registration_form}
    return render(request, 'users/auth/register.html', context)


@redirect_home_if_authenticated
def login_page(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            creds = {'username': login_form.cleaned_data['email'], 'password': login_form.cleaned_data['password']}
            user = authenticate(**creds)
            if user.is_activated == False:
                url = reverse('users:resend_activation', kwargs={'user_id': user.id}) 
                login_form.add_error('password', 
                    mark_safe(f'You haven\'t activated your account. <a href="{url}" class="text-decoration-underline">Send activation link again?</a>'))
            else:
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Hi, {user.first_name}! You have been logged in.')
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    return redirect('/')
                else:
                    login_form.add_error('password', 'Wrong password.')
    else:
        login_form = LoginForm()
    return render(request, 'users/auth/login.html', context={'form': login_form})


@redirect_home_if_authenticated
def resend_activation_email(request, user_id):
    if request.user.is_authenticated:
        return redirect('home')
    user = get_object_or_404(UserAccount, id=user_id)
    if user.is_activated == False:
        send_activation_email(request, user)
        messages.success(request, 'Please check your email, message with activation link was sent.')
    else:
        messages.warning(request, 'Your account is aleady activated.')
    return redirect('users:login')


def logout_user(request):
    logout(request)
    return redirect('users:login')


def user_profile(request, pk):
    user = get_object_or_404(UserAccount, pk=pk)
    if request.user.is_authenticated:
        if user in request.user.blacklist.blocked_users.all():
            messages.warning(request, 'You blocked this user.')
            return redirect('users:blocked')
        elif request.user in user.blacklist.blocked_users.all():
            messages.warning(request, 'This user blocked you.')
            return previous_url_or_other(request, reverse('products:home'))
    user_products = Product.active_products.filter(user=user)
    context = {'user': user, 'user_products':user_products}
    return render(request, 'users/user_profile.html', context)

@login_required
def user_dashboard(request):
    user = request.user
    purchased_products = user.purchased_products.all()
    sold_products = user.products.exclude(purchased_by=None)
    context = {'purchased_products': purchased_products, 'sold_products': sold_products}
    return render(request, 'users/dashboard.html', context)


@login_required
def edit_profile(request):
    user = get_object_or_404(UserAccount, id=request.user.id)
    if request.method == 'POST':
        edit_form = UserEditForm(request.POST, request.FILES, instance=user)
        if edit_form.is_valid():
            user = edit_form.save()
            edit_form = UserEditForm(instance=user)
    else:
        edit_form = UserEditForm(instance=user, initial = {'location': user.location })
    context = {'user': user, 'form': edit_form}
    return render(request, 'users/edit_profile.html', context)


@login_required
def remove_image(request):
    user = get_object_or_404(UserAccount, id=request.user.id)
    user.image = '../static/images/blank.jpg'
    user.save()
    messages.success(request, 'Image deleted.')
    return redirect('users:edit_profile')


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


@login_required
def add_wishlist(request, product_id):
    product = get_object_or_404(available_products(request, Product.objects), id=product_id)
    if product.user != request.user:
        wishlist = request.user.wishlist
        if product in wishlist.all():
            messages.warning(request, 'Product already in wishlist')
        else:
            wishlist.add(product)
            messages.success(request, 'Added product to your wishlist')
    return previous_url_or_other(request, reverse('products:home'))


@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist = request.user.wishlist
    if product in wishlist.all():
        wishlist.remove(product)
        messages.success(request, 'Removed product from your wishlist')
    return previous_url_or_other(request, reverse('products:detail', args=[product_id]))


@login_required
def blocked_users(request):
    blocked_users = request.user.blacklist.blocked_users.all().order_by('first_name')
    paginator = Paginator(blocked_users, 10)
    blocked_users_page = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': blocked_users_page}
    return render(request, 'users/blocked_users.html', context)


@login_required
def unblock_user(request, user_id):
    blocked_user = get_object_or_404(UserAccount, id=user_id)
    request.user.blacklist.blocked_users.remove(blocked_user)
    messages.success(request,
        f'Unblocked <a href="{blocked_user.get_absolute_url()}" class="text-decoration-underline">{blocked_user.fullname}</a>.')
    return redirect('users:blocked')


@login_required
def report_user(request, user_reported_id, message_id=None):
    report_author = request.user
    user_reported = get_object_or_404(UserAccount, id=user_reported_id)
    if user_reported in report_author.blacklist.blocked_users.all():
        messages.info(request, f'You\'ve already blocked {user_reported.fullname}.')
        return redirect('products:home')
    context = {'user_reported': user_reported}
    if message_id:
        message = get_object_or_404(Message, id=message_id, author=user_reported)
        chat = message.chat
        if report_author not in [chat.seller, chat.customer]:
            return HttpResponseForbidden()
        context['reported_message'] = message.text

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.report_author = report_author
            report.user_reported = user_reported
            report.save()

            report_author.blacklist.blocked_users.add(user_reported)

            report_author.seller_chats.filter(customer=user_reported.id).delete()
            report_author.customer_chats.filter(seller=user_reported.id).delete()
            messages.success(request, 'Report completed, thank you! Our team will take care of it.')
            return redirect('products:home')

    else:
        if message_id:
            form = ReportForm(initial={'reported_message': message_id})
        else:
            form = ReportForm()
    context['form'] = form
    return render(request, 'users/user_report.html', context)
