from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chats/(?P<chat_id>[a-z0-9]+(?:-[a-z0-9]+)*)/$', consumers.ChatConsumer.as_asgi()),
]