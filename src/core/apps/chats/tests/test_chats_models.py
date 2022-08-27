from datetime import datetime

from django.utils import timezone, dateformat 

from tests.models_setup import ModelsSetUp


class ChatTests(ModelsSetUp):
    def test_chat_participants_property(self):
        assert self.chat.participants == [self.user, self.user2]

    def test_chat_last_30_messages_property(self):
        assert self.chat.messages.first() in self.chat.last_30_messages 
    
    def test_chat_get_last_message_property(self):
        assert self.chat.get_last_message == self.message3
        self.chat.messages.all().delete()
        assert self.chat.get_last_message == None

    def test_chat_last_message_text_property(self):
        assert self.chat.last_message_text == self.message3.text
        # test message longer than 40 chars
        self.message_sys.delete()
        self.message3.delete()
        assert self.chat.last_message_text == self.message2.text[0:40] + '...'
    
    def test_chat_last_message_date_property(self):
        assert self.chat.last_message_date == self.message3.sent_date
        self.chat.messages.all().delete()
        assert self.chat.last_message_date == ''
    
    def test_chat_str_method(self):
        assert str(self.chat) == f'Chat {self.chat.seller.email}, {self.chat.customer.email} of {self.chat.product.title}' 


class MessageTests(ModelsSetUp):
    def test_message_str_method(self):
        assert str(self.message) == f'Message by {self.message.author.email} at {dateformat.format(self.message.sent_at, "d.m.y, H:i:s")}'
        assert str(self.message_sys) == f'System-generated message at {dateformat.format(self.message_sys.sent_at, "d.m.y, H:i:s")}'

    def test_message_sent_date_property(self):
        assert self.message.sent_date == dateformat.format(timezone.now(), 'H:i')

        assert self.message2.sent_date == dateformat.format(datetime.strptime('01.01.22 00:00:00', '%d.%m.%y %H:%M:%S'), 'H:i d.m')

        assert self.message3.sent_date == dateformat.format(datetime.strptime('01.01.21 00:00:00', '%d.%m.%y %H:%M:%S'), 'H:i d.m.y')