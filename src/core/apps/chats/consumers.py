import json

from django.shortcuts import get_object_or_404
from django.utils import dateformat
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from core.apps.users.models import UserAccount
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id
        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        author_id = text_data_json['authorId']
        author_name = text_data_json['authorName']
        new_message_text = text_data_json['newMessageText']
        
        author = await sync_to_async(UserAccount.objects.get)(id=author_id)
        new_message = await sync_to_async(Message.objects.create)(author=author, chat_id=self.chat_id, text=new_message_text)

        new_message_time = dateformat.format(new_message.sent_at, "H:i")
        new_message_id = new_message.id

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'author_id': author_id,
                'author_name': author_name,
                'new_message_id': new_message_id,
                'new_message_text': new_message_text,
                'new_message_time': new_message_time
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        author_id = event['author_id']
        author_name = event['author_name']
        new_message_id = event['new_message_id']
        new_message_text = event['new_message_text']
        new_message_time = event['new_message_time']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'authorId': author_id,
            'authorName': author_name,
            'newMessageId': new_message_id,
            'newMessageText': new_message_text,
            'newMessageTime': new_message_time
        }))
