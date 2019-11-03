'''当Django接受HTTP请求时，它会查询根URLconf来查找视图函数，然后调用该视图函数来处理该请求。
同样，当Channels接受WebSocket连接时，它会查询根路由配置以查找使用者，然后在使用者上调用各种功能来处理来自连接的事件。
这是一个同步的WebSocket使用者，它接受所有连接，从其客户端接收消息，并将这些消息回显到同一客户端。目前，它不会将消息广播到同一房间中的其他客户端。
'''

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))