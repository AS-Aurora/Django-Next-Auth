import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat.models import ChatRoom, Message
from django.contrib.auth import get_user_model
from channels.exceptions import StopConsumer
from django.utils import timezone
import asyncio

User = get_user_model()

class AsyncChatConsumer(AsyncWebsocketConsumer):
    # async def websocket_connect(self, event):
    #     await self.send({
    #         'type': 'websocket.accept',
    #         'text': json.dumps({'message': 'WebSocket connection established'})
    #     })
    
    # async def websocket_receive(self, event):
    #     for i in range(10):
    #         await self.send({
    #             'type': "websocket.send",
    #             'text': json.dumps({'message': f'Hello {i}'})
    #         })
    #         await asyncio.sleep(0.5)

    # async def websocket_disconnect(self, event):
    #     print("WebSocket connection closed")
    #     raise StopConsumer("WebSocket connection closed")

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.create_room_if_not_exists(self.room_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json.get('username', 'Anonymous')

        # Save the message to the database
        await self.save_message(self.room_name, username, message)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'timestamp': str(timezone.now())
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def create_room_if_not_exists(self, room_name):
        room, created = ChatRoom.objects.get_or_create(name=room_name)
        return room

    @database_sync_to_async
    def save_message(self, room_name, username, message):
        try:
            user = User.objects.get(username=username)
            room = ChatRoom.objects.get(name=room_name)
            Message.objects.create(room=room, user=user, body=message)
        except (User.DoesNotExist, ChatRoom.DoesNotExist):
            # If the user does not exist, create a default user
            pass