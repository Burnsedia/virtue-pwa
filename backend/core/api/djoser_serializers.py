from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

class UserCreateSerializer(UserCreateSerializer):
    username = serializers.CharField(required=False) # Explicitly define username

    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'email', 'username', 'password')
