import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_pk']
        self.game_group_name = 'game_%s' % self.game_name

        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name)

    def game(self, event):
        message = event['game']
        self.send(text_data=json.dumps({
            'game': message
        }))
