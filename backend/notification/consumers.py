import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from pprint import pprint


class RealTimeNotification(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.group_name = 'notification_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        self.close()

    def notify(self, event):
        self.send(text_data=json.dumps(event["text"]))
