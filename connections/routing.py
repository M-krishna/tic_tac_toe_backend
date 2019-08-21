from django.urls import path
from .consumers import CreateGameRoomConsumer

websocket_urlpatterns = [
    path('ws/create/game/room/<str:id>', CreateGameRoomConsumer)
]