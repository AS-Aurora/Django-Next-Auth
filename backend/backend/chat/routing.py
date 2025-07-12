from django.urls import path
from .consumers import AsyncChatConsumer


websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', AsyncChatConsumer.as_asgi()),
]