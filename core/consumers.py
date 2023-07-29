import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from datetime import datetime

from core.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        first_id = self.scope['user'].id
        second_id = self.scope['url_route']['kwargs']['id']
        if int(first_id) > int(second_id):
            self.room_name = f'{first_id}-{second_id}'
        else:
            self.room_name = f'{second_id}-{first_id}'

        self.room_group_name = f'{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        data_json = json.loads(text_data)
        message = data_json['message']
        username = data_json['username']

        await self.save_message(username, self.room_group_name, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = datetime.now().strftime('%H:%M')

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def save_message(self, username, title, message):
        author = User.objects.get(username=username)
        Message.objects.create(
            author=author, title=title, content=message)
