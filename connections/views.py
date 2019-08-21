from rest_framework.views import APIView
from rest_framework import status
from .serializers import GameLinkSerializer
from tic_tac_toe.response import api_response
from helpers import generate_game_link
# Create your views here.


class GenerateGameLinkView(APIView):

    @api_response
    def get(self, request):
        user = self.request.user
        game_link = generate_game_link()
        data = {
            'generated_by': user.id,
            'game_link': game_link
        }
        game_link_serializer = GameLinkSerializer(data=data)
        if game_link_serializer.is_valid():
            game_link_serializer.save()
            return {'success': 1, 'data': game_link, 'status': status.HTTP_200_OK}
