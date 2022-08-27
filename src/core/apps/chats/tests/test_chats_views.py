from django.urls import reverse
from django.contrib.messages import get_messages

from tests.models_setup import ModelsSetUp
from core.apps.chats.models import Chat


class ChatsTests(ModelsSetUp):
    def setUp(self) -> None:
        super().setUp()
        self.client.force_login(self.user)

    def test_chats_all_page(self):
        response = self.client.get(reverse('chats:all'))
        assert response.status_code == 200
        assert self.chat in response.context.get('seller_chats')
        assert not response.context.get('customer_chats')
    
    def test_enter_existing_chat(self):
        response = self.client.get(reverse('chats:detail', args=[self.chat.product.id, self.chat.id]))
        assert response.status_code == 200
        assert response.context.get('chatting_with_id') == self.user2.id
        assert response.context.get('chat') == self.chat
        # same with second user
        self.client.force_login(self.user2)
        response = self.client.get(reverse('chats:detail', args=[self.chat.product.id, self.chat.id]))
        assert response.status_code == 200
        assert response.context.get('chatting_with_id') == self.user.id
        assert response.context.get('chat') == self.chat
    
    def test_enter_existing_chat_forbidden(self):
        self.client.force_login(self.user_extra)
        response = self.client.get(reverse('chats:detail', args=[self.chat.product.id, self.chat.id]))
        assert response.status_code == 403
    
    def test_start_new_chat(self):
        self.client.force_login(self.user_extra)
        response = self.client.get(reverse('chats:detail', args=[self.chat.product.id]))
        assert response.status_code == 200
        assert response.context.get('chatting_with_id') == self.user.id
        assert response.context.get('chat')
        assert response.context.get('chat').messages.first().text == 'Negotiation started'
    
    def test_start_new_chat_forbidden_for_core(self):
        response = self.client.get(reverse('chats:detail', args=[self.product.id]))
        assert response.status_code == 302
        assert response.url == reverse('products:detail', args=[self.product.id]) 

    def test_start_new_chat_forbidden_if_blocked_by_seller(self):
        self.client.force_login(self.user_extra)
        self.user.blacklist.blocked_users.add(self.user_extra)
        response = self.client.get(reverse('chats:detail', args=[self.product.id]))
        assert response.status_code == 302
        assert response.url == reverse('products:home')

    def test_start_new_chat_forbidden_if_blocked_seller(self):
        self.client.force_login(self.user_extra)
        self.user_extra.blacklist.blocked_users.add(self.user)
        response = self.client.get(reverse('chats:detail', args=[self.product.id]))
        assert response.status_code == 302
        assert response.url == reverse('users:blocked')

    def test_delete_chat_success(self):
        response = self.client.get(reverse('chats:delete', args=[self.chat.id]))
        assert response.status_code == 302
        assert response.url == reverse('chats:all')
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == 'Chat deleted.'
    
    def test_delete_chat_redirect_if_not_allowed(self):
        self.client.force_login(self.user_extra)
        response = self.client.get(reverse('chats:delete', args=[self.chat.id]))
        assert response.status_code == 302
        assert response.url == reverse('products:detail', args=[self.product.id]) 

    def test_read_message_success(self):
        response = self.client.get(reverse('chats:read_message', args=[self.message.id]))
        assert response.status_code == 200
        self.message.refresh_from_db()
        assert self.message.is_seen == True
        assert response.json() == {'success': True}

    def test_read_message_forbidden(self):
        # message's author tries to read it
        self.client.force_login(self.user2)
        # actual user to whom the message was sent reads it
        response = self.client.get(reverse('chats:read_message', args=[self.message.id]))
        assert response.status_code == 403
        self.message.refresh_from_db()
        assert self.message.is_seen == False

    def test_request_done_deal_success(self):
        response = self.client.get(reverse('chats:request_done_deal', args=[self.chat.id]))
        assert response.status_code == 302
        assert response.url == reverse('chats:detail', args=[self.product.id, self.chat.id])
        self.chat.refresh_from_db()
        assert self.chat.done_deal_requested == True 
        assert self.chat.messages.last().text == 'Seller marked this deal as done, if it\'s true customer should confirm it by clicking button on the panel'

    def test_request_done_deal_forbidden(self):
        # seller requests done deal
        self.client.force_login(self.user2)
        response = self.client.get(reverse('chats:request_done_deal', args=[self.chat.id]))
        assert response.status_code == 403
    
    def test_request_done_deal_cancel_success(self):
        self.client.get(reverse('chats:request_done_deal', args=[self.chat.id]))
        response = self.client.get(reverse('chats:request_done_deal_cancel', args=[self.chat.id]))
        assert response.status_code == 302
        assert response.url == reverse('chats:detail', args=[self.product.id, self.chat.id])
        self.chat.refresh_from_db()
        assert self.chat.done_deal_requested == False 
        assert self.chat.messages.last().text != 'Seller marked this deal as done, if it\'s true customer should confirm it by clicking button on the panel'
    
    def test_request_done_deal_cancel_forbidden(self):
        # customer tries to cancel the done deal request
        self.client.force_login(self.user2)
        response = self.client.get(reverse('chats:request_done_deal_cancel', args=[self.chat.id]))
        assert response.status_code == 403
    
    def test_confirm_deal_success(self):
        # firstly seller requests done deal
        response = self.client.get(reverse('chats:request_done_deal', args=[self.chat.id]))
        # cutomer confirms
        self.client.force_login(self.user2)
        response = self.client.get(reverse('chats:confirm_deal', args=[self.chat.id]))
        assert response.status_code == 302
        self.product.refresh_from_db()
        assert self.product.purchased_by == self.user2
        assert not Chat.objects.all()        
        messages = list(get_messages(response.wsgi_request))
        assert str(messages[0]) == 'We\'re happy you completed a purchase via our website!'

    def test_confirm_deal_forbidden(self):
        # seller requests done deal
        response = self.client.get(reverse('chats:request_done_deal', args=[self.chat.id]))
        # and then tries to confirm himself
        response = self.client.get(reverse('chats:confirm_deal', args=[self.chat.id]))
        assert response.status_code == 403
    
    def test_check_for_new_messages_success(self):
        response = self.client.get(reverse('chats:check_for_new_messages'))
        assert response.status_code == 200
        assert response.json().get('newMessagesCount') == 4
