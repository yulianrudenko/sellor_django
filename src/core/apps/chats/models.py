import uuid
import datetime

from django.db import models
from django.utils import timezone, dateformat

from core.apps.users.models import UserAccount
from core.apps.products.models import Product
from django.db.models import Q


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, related_name='chats', on_delete=models.CASCADE, null=True)
    seller = models.ForeignKey(UserAccount, related_name='seller_chats', on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(UserAccount, related_name='customer_chats', on_delete=models.SET_NULL, null=True)
    started_at = models.DateTimeField(default=timezone.now, editable=False)
    done_deal_requested = models.BooleanField(default=False)

    @property
    def sellers_unseen_messages_count(self) -> int:
        return int(self.messages.filter(Q(is_seen=False) & (Q(author=self.customer) | Q(is_system_generated=True))).count())

    @property
    def customers_unseen_messages_count(self) -> int:
        return int(self.messages.filter(Q(is_seen=False) & (Q(author=self.seller) | Q(is_system_generated=True))).count())

    @property
    def participants(self) -> list:
        return [self.seller, self.customer]

    @property
    def last_30_messages(self):
        return reversed(self.messages.order_by('-sent_at')[:30])
    
    @property
    def get_last_message(self) -> object:
        if self.messages.last():
            return self.messages.last()
        return None

    @property
    def last_message_text(self) -> str:
        last_msg = self.get_last_message.text or ''
        if len(last_msg) > 40:
            return last_msg[0:40] + '...'
        return last_msg
    
    @property
    def last_message_date(self) -> str:
        if self.get_last_message:
            return self.get_last_message.sent_date
        return ''
    
    def __str__(self) -> str:
        return f'Chat {self.seller.email}, {self.customer.email} of {self.product.title}'


class Message(models.Model):
    author = models.ForeignKey(UserAccount, related_name='messages', on_delete=models.SET_NULL, null=True)
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    sent_at = models.DateTimeField(default=timezone.now, editable=False)
    is_system_generated = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    @property
    def sent_date(self):
        current_date = str(datetime.datetime.now().date())
        date_sent = dateformat.format(self.sent_at, "Y-m-d")    
        if current_date == date_sent:
            return dateformat.format(self.sent_at, "H:i")

        current_year = str(datetime.datetime.now().year)
        year_sent = dateformat.format(self.sent_at, "Y")
        if year_sent == current_year:
            return dateformat.format(self.sent_at, "H:i d.m")
        return dateformat.format(self.sent_at, "H:i d.m.y")

    def __str__(self) -> str:
        if not self.is_system_generated:
            return f'Message by {self.author.email} at {dateformat.format(self.sent_at, "d.m.y, H:i:s")}'
        return f'System-generated message at {dateformat.format(self.sent_at, "d.m.y, H:i:s")}'
