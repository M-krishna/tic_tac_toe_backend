from rest_framework import serializers

from helpers import generate_unique_name
from .models import User, ActivationLink


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def create(self, validated_data):
        unique_name = generate_unique_name(validated_data['first_name'])
        user = User.objects.create_user(username=validated_data['email'],
                                        first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'],
                                        email=validated_data['email'],
                                        is_active=False,
                                        unique_name=unique_name
                                        )
        user.set_password(self.initial_data['password'])
        user.save()
        return user


class UserActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivationLink
        fields = '__all__'
