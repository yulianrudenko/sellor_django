from django.urls import path

from . import views


app_name = 'chats'

urlpatterns = [
    path('', views.chats_all, name='all'),
    path('<slug:product_id>_<slug:chat_id>/', views.enter_chat, name='detail'),
    path('<slug:product_id>/', views.enter_chat, name='detail'),
    path('<slug:chat_id>/delete', views.delete_chat, name='delete'),
    path('<slug:chat_id>/request-done-deal', views.request_done_deal, name='request_done_deal'),
    path('<slug:chat_id>/request-done-deal-cancel', views.request_done_deal_cancel, name='request_done_deal_cancel'),
    path('<slug:chat_id>/confirm-deal', views.confirm_deal, name='confirm_deal'),
    path('<slug:message_id>/read', views.read_message, name='read_message'),

    path('check-for-messages', views.check_for_new_messages, name='check_for_new_messages'),
    path('check-for-done-deal-request/<slug:chat_id>', views.check_for_done_deal_request, name='check_for_done_deal_request'),
    path('check-for-confirm-deal/<int:customer_id>', views.check_for_confirm_deal, name='check_for_confirm_deal'),
]
