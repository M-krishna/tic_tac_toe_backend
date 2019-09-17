import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from connections.models import GameLinkModel


class CreateGameRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_room_id = str(self.scope['url_route']['kwargs']['id'])
        self.link = await database_sync_to_async(self.check_game_link)(self.game_room_id)

        if self.link:
            await self.channel_layer.group_add(
                self.game_room_id,
                self.channel_name
            )

            await self.accept()

            await self.send(text_data=json.dumps({
                'message': 'connected'
            }))
        else:

            await self.close()

    async def disconnect(self, code):

        await self.channel_layer.group_discard(
            self.game_room_id,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        await self.send('Hello There')

    # Checking the Game Room Channel exists in db
    @staticmethod
    def check_game_link(game_link):
        link = GameLinkModel.objects.filter(game_link=game_link)
        if link:
            return True
        return False
