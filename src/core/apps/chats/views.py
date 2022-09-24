from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils.translation import gettext_lazy as _

from core.apps.products.models import Product
from core.apps.users.models import UserAccount
from .models import Chat, Message


@login_required
def chats_all(request):
    seller_chats = Chat.objects.filter(seller=request.user)
    seller_chats = sorted(seller_chats, key=lambda chat: (chat.get_last_message.sent_at, chat.done_deal_requested))
    seller_chats.reverse()
    customer_chats = Chat.objects.filter(customer=request.user)
    customer_chats = sorted(customer_chats, key=lambda chat: (chat.get_last_message.sent_at, chat.done_deal_requested))
    customer_chats.reverse()
    context = {'seller_chats': seller_chats, 'customer_chats': customer_chats}
    return render(request, 'chats/all_chats.html', context)


@login_required
def enter_chat(request, product_id, chat_id=None):
    user = request.user
    context = {'chatting_with_id': ''}
    if chat_id:
        chat = get_object_or_404(Chat, id=chat_id)
        if user == chat.seller:
            context['chatting_with_id'] = chat.customer.id
        elif user == chat.customer:
            context['chatting_with_id'] = chat.seller.id
        else:
            return HttpResponseForbidden('You don\'t have permission to access this resource')

    else:
        product = get_object_or_404(Product, id=product_id)
        seller = product.user
        if user == seller: 
            return redirect('products:detail', product.id)
        # user is customer starting or entering a chat
        # validate if user is blocked by seller or has blocked seller
        if user.is_blocked_by(seller):
            messages.warning(request, _('You cannot start conversation with this user.'))
            return redirect('products:home')
        if user.has_blocked(seller):
            messages.warning(request, _('You blocked this user.'))
            return redirect('users:blocked')
        chat, created = Chat.objects.get_or_create(product=product, seller=seller, customer=user)
        if created:
            message = Message.objects.create(is_system_generated=True, chat=chat, text='Chat created. Customer now should start conversation.', author=None, is_seen=False)
            message.save()
        context['chatting_with_id'] = chat.seller.id

    chat.messages.exclude(author=request.user).update(is_seen=True)
    context['chat'] = chat
    return render(request, 'chats/detail_chat.html', context)


@login_required
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user not in [chat.seller, chat.customer]:
        return redirect('products:detail', chat.product.id)
    chat.delete()
    messages.success(request, _('Chat deleted.'))
    return redirect('chats:all')


@login_required
def read_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user not in message.chat.participants or request.user == message.author:
        return HttpResponseForbidden('You don\'t have permission to access this resource')
    message.is_seen = True
    message.save()
    return JsonResponse({'success': True})


@login_required
def request_done_deal(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.seller:
        if not chat.done_deal_requested == True:
            chat.done_deal_requested = True
            Message.objects.create(
                chat=chat, is_system_generated=True,
                text='Seller marked this deal as done, if it\'s true customer should confirm it by clicking button on the panel', author=None)
            chat.save()
        return redirect('chats:detail', chat.product.id, chat_id)
    return HttpResponseForbidden('You don\'t have permission to access this resource')


@login_required
def request_done_deal_cancel(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.seller:
        chat.done_deal_requested = False
        Message.objects.filter(
            chat=chat, is_system_generated=True,
            text='Seller marked this deal as done, if it\'s true customer should confirm it by clicking button on the panel', author=None).delete()
        chat.save()
        return redirect('chats:detail', chat.product.id, chat_id)
    return HttpResponseForbidden('You don\'t have permission to access this resource')


@login_required
def confirm_deal(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    if request.user == chat.customer and chat.done_deal_requested == True:
        chat.product.purchased_by = request.user
        chat.product.save()
        chat.delete()
        messages.success(request, _('We\'re happy you completed a purchase via our website!'))
        return redirect('users:dashboard')
    return HttpResponseForbidden('You don\'t have permission to access this resource')


@login_required
def check_for_new_messages(request):
    return JsonResponse({'newMessagesCount': request.user.unseen_messages_count})


@login_required
def check_for_done_deal_request(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, customer=request.user)
    return JsonResponse({'is_requested': chat.done_deal_requested})


@login_required
def check_for_confirm_deal(request, customer_id):
    customer = get_object_or_404(UserAccount, pk=customer_id)
    if request.user.products.filter(purchased_by=customer).exists():
        return JsonResponse({'is_confirmed': 'true'})
    return JsonResponse({'is_confirmed': 'false'})