from channels.generic.websocket import AsyncWebsocketConsumer
import json


class CreateGameRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_room_id = self.scope['url_route']['kwargs']['id']

        await self.channel_layer.group_add(
            self.game_room_id,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': 'connected'
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.game_room_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        await self.send('Hello There')