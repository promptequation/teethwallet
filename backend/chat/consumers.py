import json

from api.models.user_model import User
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core import serializers

from .models import Connection, Conversation


class ChatConsumer(AsyncWebsocketConsumer):
    isEdited = False

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope['user']

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
        conversation_instance = await self.save_message(json.loads(text_data))
        conversation = serializers.serialize('json', [conversation_instance])
        # user = serializers.serialize('json', [self.user])

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'conversation': conversation,
                # 'user': user,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'conversation': event['conversation'],
            'connection': self.room_name,
            'edited': self.isEdited
            # 'user': event['user']
        }))

    @database_sync_to_async
    def save_message(self, message):
        created_by = User.objects.get(pk=message['created_by'])
        updated_by = User.objects.get(pk=message['updated_by'])
        sender = User.objects.get(pk=message['sender'])
        receiver = User.objects.get(pk=message['receiver'])
        connection = Connection.objects.get(pk=message['connection'])

        try:
            conversation = Conversation.objects.get(id=message['id'])

            conversation.message = message['message']
            conversation.is_seen = message['is_seen']
            conversation.is_edited = message['is_edited']

            try:
                conversation.save()
            except Exception as e:
                pass

            self.isEdited = True

            if conversation:
                return conversation
            else:
                self.disconnect(0)

        except Exception as e:
            message_instance = Conversation.objects.create(
                connection=connection,
                message=message['message'],
                sender=sender,
                receiver=receiver,
                is_seen=message['is_seen'],
                is_edited=message['is_edited'],
                is_auto_message=message['is_auto_message'],
                created_by=created_by,
                updated_by=updated_by,
            )

            self.isEdited = False

            if message_instance:
                return message_instance
            else:
                self.disconnect(0)
