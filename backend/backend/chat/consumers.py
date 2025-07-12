import json
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
import asyncio

class AsyncChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept',
            'text': json.dumps({'message': 'WebSocket connection established'})
        })
    
    async def websocket_receive(self, event):
        for i in range(10):
            await self.send({
                'type': "websocket.send",
                'text': json.dumps({'message': f'Hello {i}'})
            })
            await asyncio.sleep(0.5)

    async def websocket_disconnect(self, event):
        print("WebSocket connection closed")
        raise StopConsumer("WebSocket connection closed")