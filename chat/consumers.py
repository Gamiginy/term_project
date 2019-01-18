from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Chat
import json


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        # 元のコードは→self.room_group_name = 'chat_%s' % self.room_name
        self.room_group_name = 'chat_{}'.format(self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data, **kwargs):
        text_data_json = json.loads(text_data)
        user_name = text_data_json['user_name']
        message = '[' + user_name + ']: '
        message += text_data_json['message']
        room_name = text_data_json['room_name']

        Chat.objects.create(message=message, book_id=room_name)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'from_user_name': user_name,
                'room_name': room_name,
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        user_name = event['from_user_name']
        room_name = event['room_name']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'from_user_name': user_name,
            'room_name': room_name,
        }))