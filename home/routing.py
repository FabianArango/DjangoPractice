from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path("ws/chat/(?P<AppRoomName>\w+)/", consumers.ChatConsumer.as_asgi(), name="some"),
    re_path("ws/userChat/(?P<chatId>\w+)", consumers.UserChat.as_asgi()),
    re_path("ws/RoomServer/(?P<room>\w+)", consumers.RoomServer.as_asgi())
]