from rest_framework import serializers
from .models import GameLinkModel


class GameLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameLinkModel
        fields = '__all__'
