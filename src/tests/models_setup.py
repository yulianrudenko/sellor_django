import uuid
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import connection
from django.db.models.signals import (
    pre_init, post_init,
    pre_save, post_save,
    pre_delete, post_delete,
    pre_migrate, post_migrate,
)

from collections import defaultdict

from core.apps.products.models import (
    Product,
    Category,
    Tag
)
from core.apps.users.models import Blacklist, City
from core.apps.chats.models import Chat, Message

User = get_user_model()
product_uid = uuid.uuid4()
product_uid2 = uuid.uuid4()


# class to disable all signals
class DisableSignals(object):
    def __init__(self, disabled_signals=None):
        self.stashed_signals = defaultdict(list)
        self.disabled_signals = disabled_signals or [
            pre_init, post_init,
            pre_save, post_save,
            pre_delete, post_delete,
            pre_migrate, post_migrate,
        ]

    def __enter__(self):
        for signal in self.disabled_signals:
            self.disconnect(signal)

    def __exit__(self, exc_type, exc_val, exc_tb):
        for signal in list(self.stashed_signals):
            self.reconnect(signal)

    def disconnect(self, signal):
        self.stashed_signals[signal] = signal.receivers
        signal.receivers = []

    def reconnect(self, signal):
        signal.receivers = self.stashed_signals.get(signal, [])
        del self.stashed_signals[signal]


class ModelsSetUp(TestCase):
    def setUp(self) -> None:
        with DisableSignals():
            # restarting the table sequence so category will have id=1 for each test   
            with connection.cursor() as cursor:
                cursor.execute("ALTER SEQUENCE products_category_id_seq RESTART WITH 1;")
            self.category = Category.objects.create(name='test_category')
            self.tag = Tag.objects.create(name='test_tag')

        self.city = City.objects.create(name='test_city')
        
        # dict for form tests
        self.credentials = {
            'email': 'user@gmail.com',
            'first_name': 'officer',
            'last_name': 'key',
            'password': '123456',
            'gender': 'M',
            'location': self.city,
        }
        self.user = User.objects.create(**self.credentials)
        self.user.set_password(self.credentials['password'])
        self.user.save()
        
        self.user2 = User.objects.create(
            email='user2@gmail.com',
            first_name='lionel',
            last_name='messi',
            gender='M',
            location=self.city,
        )
        self.user2.set_password(self.credentials['password'])
        self.user2.save()

        
        self.product = Product.objects.create(
            id=product_uid,
            user=self.user,
            category=self.category,
            title='test_product',
            price=50,
            discount_price=40,
            description='description for test_product'
        )
        self.product.tags.add(self.tag)
        self.product2 = Product.objects.create(
            id=product_uid2,
            user=self.user,
            category=self.category,
            title='test_product2',
            price=10,
            description='description for test_product2',
            purchased_by=self.user2
        )

        self.chat = Chat.objects.create(
            product=self.product,
            seller=self.user,
            customer=self.user2
        )
        self.message_sys = Message.objects.create(
            chat=self.chat,
            text='test',
            is_system_generated=True
        )
        self.message = Message.objects.create(
            author=self.user2,
            chat=self.chat,
            text='test_text',
            is_seen=False
        )
        self.message2 = Message.objects.create(
            author=self.user2,
            chat=self.chat,
            text=str('longMsg' * 6),
            is_seen=False,
            sent_at=datetime.strptime('01.01.22 00:00:00', '%d.%m.%y %H:%M:%S')
        )
        self.message3 = Message.objects.create(
            author=self.user2,
            chat=self.chat,
            text='test_text3',
            is_seen=False,
            sent_at=datetime.strptime('01.01.21 00:00:00', '%d.%m.%y %H:%M:%S')
        )

        self.user_extra = User.objects.create(
            email='user_extra@gmail.com',
            first_name='extra',
            last_name='user',
            gender='X',
            location=self.city,
        )
        self.user_extra.set_password(self.credentials['password'])
        self.user_extra.save()
